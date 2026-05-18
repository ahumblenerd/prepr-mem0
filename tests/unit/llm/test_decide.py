from __future__ import annotations

import json
from uuid import uuid4

import httpx
import pytest
import respx

from prepr_mem0.config import Settings
from prepr_mem0.db.repo import Neighbor
from prepr_mem0.llm.decide import decide_actions


def _completion_response(content: str) -> dict:
    return {
        "id": "x",
        "object": "chat.completion",
        "created": 0,
        "model": "test",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            },
        ],
    }


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_empty_neighbors_means_all_add(respx_mock: respx.MockRouter):
    respx_mock.post("/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json=_completion_response(
                json.dumps(
                    {
                        "memory": [
                            {"id": "0", "text": "fact one", "event": "ADD"},
                            {"id": "1", "text": "fact two", "event": "ADD"},
                        ]
                    }
                )
            ),
        )
    )
    actions = await decide_actions(["fact one", "fact two"], [[], []])
    assert [a.event for a in actions] == ["ADD", "ADD"]
    assert [a.fact for a in actions] == ["fact one", "fact two"]
    assert all(a.target_memory_id is None for a in actions)


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_remaps_uuids_to_small_ints_in_prompt(respx_mock: respx.MockRouter):
    captured: dict = {}
    neighbor_id = uuid4()

    def _record(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            json=_completion_response(
                json.dumps({"memory": [{"id": "0", "text": "x", "event": "NONE"}]})
            ),
        )

    respx_mock.post("/chat/completions").mock(side_effect=_record)
    neighbors = [[Neighbor(memory_id=neighbor_id, content="x", distance=0.1)]]
    await decide_actions(["x"], neighbors)

    user_msg = captured["body"]["messages"][-1]["content"]
    assert str(neighbor_id) not in user_msg  # raw UUID never reaches the LLM
    assert "'id': '0'" in user_msg or '"id": "0"' in user_msg or "'id':'0'" in user_msg


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_remaps_response_back_to_uuids(respx_mock: respx.MockRouter):
    neighbor_uuid = uuid4()
    respx_mock.post("/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json=_completion_response(
                json.dumps(
                    {
                        "memory": [
                            {
                                "id": "0",
                                "text": "updated fact",
                                "event": "UPDATE",
                                "old_memory": "x",
                            },
                            {"id": "1", "text": "new fact", "event": "ADD"},
                        ]
                    }
                )
            ),
        )
    )
    neighbors = [
        [Neighbor(memory_id=neighbor_uuid, content="x", distance=0.05)],
        [],
    ]
    actions = await decide_actions(["updated fact", "new fact"], neighbors)

    update = next(a for a in actions if a.event == "UPDATE")
    add = next(a for a in actions if a.event == "ADD")
    assert update.target_memory_id == neighbor_uuid
    assert add.target_memory_id is None


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_dedupes_neighbors_across_facts(respx_mock: respx.MockRouter):
    """The same UUID showing up in two facts' neighbor lists must remap to a single id."""
    captured: dict = {}
    shared = uuid4()

    def _record(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            json=_completion_response(
                json.dumps({"memory": [{"id": "0", "text": "x", "event": "NONE"}]})
            ),
        )

    respx_mock.post("/chat/completions").mock(side_effect=_record)
    neighbors = [
        [Neighbor(memory_id=shared, content="x", distance=0.01)],
        [Neighbor(memory_id=shared, content="x", distance=0.01)],
    ]
    await decide_actions(["a", "b"], neighbors)
    user_msg = captured["body"]["messages"][-1]["content"]
    # only one remapped entry for the shared memory
    assert user_msg.count("'text': 'x'") + user_msg.count('"text": "x"') == 1


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_unknown_id_in_response_is_dropped(respx_mock: respx.MockRouter):
    """If the LLM emits an id we never sent, drop the action rather than crash."""
    respx_mock.post("/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json=_completion_response(
                json.dumps(
                    {
                        "memory": [
                            {"id": "99", "text": "ghost", "event": "UPDATE"},
                            {"id": "0", "text": "real", "event": "ADD"},
                        ]
                    }
                )
            ),
        )
    )
    actions = await decide_actions(["real"], [[]])
    assert [a.event for a in actions] == ["ADD"]
    assert actions[0].fact == "real"


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url, assert_all_called=False)
async def test_no_facts_short_circuits(respx_mock: respx.MockRouter):
    """No facts means no LLM call and no actions."""
    route = respx_mock.post("/chat/completions")
    actions = await decide_actions([], [])
    assert actions == []
    assert route.call_count == 0
