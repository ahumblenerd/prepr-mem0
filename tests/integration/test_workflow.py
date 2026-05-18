"""End-to-end tests for the add_memory workflow body.

These run against:

- a real Postgres (the live tmpfs one in compose)
- a real respx-mocked OpenRouter at the httpx layer
- a FakeContext that runs each `ctx.run` action eagerly with no journaling

That's enough to validate the pipeline: create_event -> facts -> knn ->
decide -> apply -> finish_event all touch the right tables. The full
Restate path (with journaled replay) is covered by Phase 6's chaos test
which has to use a real sidecar anyway.
"""

from __future__ import annotations

import json
from typing import Any
from uuid import uuid4

import httpx
import pytest
import respx
from sqlalchemy import select

from prepr_mem0.config import Settings
from prepr_mem0.db.models import AddEvent, Memory, MemoryHistory
from prepr_mem0.llm.openrouter import reset_client_for_tests
from prepr_mem0.schemas.api import AddRequest, Message, MessageRole
from prepr_mem0.workflow import _steps
from prepr_mem0.workflow.add_memory import run_add_memory


class FakeCtx:
    """Same shape as the unit-test FakeContext but with no canned outputs —
    every `ctx.run` actually executes its action."""

    def __init__(self, key: str) -> None:
        self._key = key

    def key(self) -> str:
        return self._key

    async def run(self, _name: str, action: Any) -> Any:
        out = action()
        if hasattr(out, "__await__"):
            out = await out
        return out


def _completion(content: str) -> dict:
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


@pytest.fixture(autouse=True)
def openrouter_env(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    reset_client_for_tests()
    yield
    reset_client_for_tests()


@pytest.fixture
def user_id() -> str:
    return f"e2e-{uuid4().hex[:8]}"


async def test_full_pipeline_writes_memories_and_history(session, user_id):
    event_id = uuid4()
    req = AddRequest(
        user_id=user_id,
        messages=[Message(role=MessageRole.user, content="My name is Alice and I like tea.")],
    )

    base = Settings.from_env().openrouter_base_url
    with respx.mock(base_url=base) as mock:
        mock.post("/chat/completions").mock(
            side_effect=[
                # 1) extract_facts
                httpx.Response(
                    200,
                    json=_completion(json.dumps({"facts": ["Name is Alice", "Likes tea"]})),
                ),
                # 2) decide_actions — both fresh facts -> both ADD
                httpx.Response(
                    200,
                    json=_completion(
                        json.dumps(
                            {
                                "memory": [
                                    {"id": "0", "text": "Name is Alice", "event": "ADD"},
                                    {"id": "1", "text": "Likes tea", "event": "ADD"},
                                ]
                            }
                        )
                    ),
                ),
            ]
        )
        result = await run_add_memory(FakeCtx(str(event_id)), req)

    assert result.event_id == event_id
    assert result.status == "SUCCEEDED"

    # Event row finished SUCCEEDED with two ADD entries.
    row = await session.get(AddEvent, event_id)
    assert row is not None
    assert row.status == "SUCCEEDED"
    assert row.latency_ms is not None
    assert row.latency_ms >= 0
    assert len(row.result) == 2
    assert {entry["event"] for entry in row.result} == {"ADD"}

    # Memories present.
    mems = (await session.execute(select(Memory).where(Memory.user_id == user_id))).scalars().all()
    assert len(mems) == 2
    assert {m.content for m in mems} == {"Name is Alice", "Likes tea"}

    # History row per memory.
    hist = (await session.execute(select(MemoryHistory))).scalars().all()
    add_events = [h for h in hist if h.event == "ADD"]
    assert len(add_events) == 2


async def test_reconcile_skips_duplicate_when_llm_decides_none(session, user_id):
    """If decide_actions returns NONE for an existing memory, no new row is written."""
    # Seed an existing memory so knn returns a neighbor.
    seeded = Memory(
        user_id=user_id,
        content="Name is Alice",
        content_hash="seed",
        embedding=[0.0] * 1536,
    )
    session.add(seeded)
    await session.commit()
    await session.refresh(seeded)

    event_id = uuid4()
    req = AddRequest(
        user_id=user_id,
        messages=[Message(role=MessageRole.user, content="My name is Alice.")],
    )

    base = Settings.from_env().openrouter_base_url
    with respx.mock(base_url=base) as mock:
        mock.post("/chat/completions").mock(
            side_effect=[
                httpx.Response(
                    200,
                    json=_completion(json.dumps({"facts": ["Name is Alice"]})),
                ),
                # decide_actions remaps the seeded UUID to "0", LLM says NONE.
                httpx.Response(
                    200,
                    json=_completion(
                        json.dumps(
                            {"memory": [{"id": "0", "text": "Name is Alice", "event": "NONE"}]}
                        )
                    ),
                ),
            ]
        )
        await run_add_memory(FakeCtx(str(event_id)), req)

    mems = (await session.execute(select(Memory).where(Memory.user_id == user_id))).scalars().all()
    # Still just the one seeded memory — no duplicate ADD.
    assert len(mems) == 1
    assert mems[0].id == seeded.id


async def test_failed_apply_actions_leaves_event_unfinished(session, user_id):
    """If apply_actions raises, the event status stays PENDING (Restate would retry).

    The fake context just propagates the exception; we assert state is clean.
    """
    event_id = uuid4()
    req = AddRequest(
        user_id=user_id,
        messages=[Message(role=MessageRole.user, content="Likes coffee.")],
    )

    # Patch apply_actions_step to blow up.
    orig = _steps.apply_actions_step

    async def _boom(*_args, **_kwargs):
        msg = "simulated db crash mid-tx"
        raise RuntimeError(msg)

    _steps.apply_actions_step = _boom  # type: ignore[assignment]

    base = Settings.from_env().openrouter_base_url
    try:
        with respx.mock(base_url=base) as mock:
            mock.post("/chat/completions").mock(
                side_effect=[
                    httpx.Response(200, json=_completion(json.dumps({"facts": ["Likes coffee"]}))),
                    httpx.Response(
                        200,
                        json=_completion(
                            json.dumps(
                                {"memory": [{"id": "0", "text": "Likes coffee", "event": "ADD"}]}
                            )
                        ),
                    ),
                ]
            )
            with pytest.raises(RuntimeError, match="simulated"):
                await run_add_memory(FakeCtx(str(event_id)), req)
    finally:
        _steps.apply_actions_step = orig  # type: ignore[assignment]

    # No memories written for this user.
    mems = (await session.execute(select(Memory).where(Memory.user_id == user_id))).scalars().all()
    assert len(mems) == 0
    # Event row exists and is still PENDING (create_event ran; finish_event did not).
    row = await session.get(AddEvent, event_id)
    assert row is not None
    assert row.status == "PENDING"
