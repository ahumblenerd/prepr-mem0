from __future__ import annotations

import json

import httpx
import pytest
import respx

from prepr_mem0.config import Settings
from prepr_mem0.llm.extract import extract_facts
from prepr_mem0.schemas.api import Message, MessageRole


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


@pytest.fixture
def messages():
    return [Message(role=MessageRole.user, content="My name is Arun and I drink earl grey.")]


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_parses_clean_json_response(respx_mock: respx.MockRouter, messages):
    respx_mock.post("/chat/completions").mock(
        return_value=httpx.Response(
            200, json=_completion_response(json.dumps({"facts": ["a", "b"]}))
        )
    )
    out = await extract_facts(messages)
    assert out == ["a", "b"]


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_strips_fences(respx_mock: respx.MockRouter, messages):
    respx_mock.post("/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json=_completion_response('```json\n{"facts": ["wrapped"]}\n```'),
        )
    )
    assert await extract_facts(messages) == ["wrapped"]


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_strips_think_tags(respx_mock: respx.MockRouter, messages):
    respx_mock.post("/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json=_completion_response('<think>reasoning</think>{"facts": ["c"]}'),
        )
    )
    assert await extract_facts(messages) == ["c"]


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_normalizes_dict_facts(respx_mock: respx.MockRouter, messages):
    respx_mock.post("/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json=_completion_response(json.dumps({"facts": [{"fact": "x"}, {"text": "y"}, "z"]})),
        )
    )
    assert await extract_facts(messages) == ["x", "y", "z"]


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_retries_on_429(respx_mock: respx.MockRouter, messages):
    route = respx_mock.post("/chat/completions").mock(
        side_effect=[
            httpx.Response(429, json={"error": "rate-limited"}),
            httpx.Response(200, json=_completion_response('{"facts": ["after-retry"]}')),
        ]
    )
    out = await extract_facts(messages)
    assert out == ["after-retry"]
    assert route.call_count == 2


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_user_prompt_carries_only_user_messages(respx_mock: respx.MockRouter):
    captured: dict = {}

    def _record(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json=_completion_response('{"facts": []}'))

    respx_mock.post("/chat/completions").mock(side_effect=_record)
    msgs = [
        Message(role=MessageRole.system, content="you are helpful"),
        Message(role=MessageRole.user, content="hi"),
        Message(role=MessageRole.assistant, content="hello back"),
    ]
    await extract_facts(msgs)
    body = captured["body"]
    # System prompt + user prompt with transcript
    assert body["messages"][0]["role"] == "system"
    assert body["messages"][1]["role"] == "user"
    assert "user: hi" in body["messages"][1]["content"]
    # JSON response mode requested for parser stability
    assert body.get("response_format") == {"type": "json_object"}


@pytest.mark.respx(base_url=Settings.from_env().openrouter_base_url)
async def test_uses_agent_prompt_when_agent_id_set(respx_mock: respx.MockRouter):
    captured: dict = {}

    def _record(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json=_completion_response('{"facts": []}'))

    respx_mock.post("/chat/completions").mock(side_effect=_record)
    msgs = [Message(role=MessageRole.user, content="hi")]
    await extract_facts(msgs, agent_id="agent-1")
    system = captured["body"]["messages"][0]["content"]
    assert "Assistant Information Organizer" in system
