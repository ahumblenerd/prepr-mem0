"""Unit tests for the add_memory workflow body, driven by a fake Context.

These tests don't need Restate or Postgres — they prove the workflow calls
the right side-effect steps in the right order with the right arguments.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

import pytest

from prepr_mem0.schemas.api import AddRequest, Message, MessageRole
from prepr_mem0.workflow.add_memory import run_add_memory


@dataclass
class FakeContext:
    """Mimics the subset of restate.WorkflowContext the workflow body uses."""

    workflow_key: str
    canned: dict[str, Any] = field(default_factory=dict)
    calls: list[str] = field(default_factory=list)
    call_args: dict[str, Any] = field(default_factory=dict)

    def key(self) -> str:
        return self.workflow_key

    async def run(
        self,
        name: str,
        action: Callable[[], Any] | Callable[[], Awaitable[Any]],
    ) -> Any:
        self.calls.append(name)
        # Execute the action so prompt/arg captures get exercised, but ignore
        # any DB / LLM errors — these tests just want step-ordering proof.
        try:
            result = action()
            if hasattr(result, "__await__"):
                result = await result
            self.call_args[name] = result
        except Exception as exc:  # noqa: BLE001 — fake context tolerates anything
            self.call_args[name] = exc
        # Canned override always wins.
        if name in self.canned:
            return self.canned[name]
        return self.call_args[name]


@pytest.fixture
def req() -> AddRequest:
    return AddRequest(
        user_id="alice",
        agent_id=None,
        run_id=None,
        messages=[Message(role=MessageRole.user, content="My name is Alice.")],
    )


async def test_step_order_with_no_facts(req: AddRequest):
    event_id = uuid4()
    ctx = FakeContext(
        workflow_key=str(event_id),
        canned={
            "create_event": None,
            "extract_facts": [],
            "decide_actions": [],
            "apply_actions": [],
            "finish_event": None,
        },
    )
    result = await run_add_memory(ctx, req)
    assert ctx.calls == [
        "create_event",
        "extract_facts",
        "decide_actions",
        "apply_actions",
        "finish_event",
    ]
    assert result.event_id == event_id
    assert result.status == "SUCCEEDED"


async def test_step_order_with_facts_includes_per_fact_knn(req: AddRequest):
    event_id = uuid4()
    ctx = FakeContext(
        workflow_key=str(event_id),
        canned={
            "create_event": None,
            "extract_facts": ["fact one", "fact two"],
            "knn:0": [],
            "knn:1": [],
            "decide_actions": [],
            "apply_actions": [],
            "finish_event": None,
        },
    )
    await run_add_memory(ctx, req)
    assert ctx.calls == [
        "create_event",
        "extract_facts",
        "knn:0",
        "knn:1",
        "decide_actions",
        "apply_actions",
        "finish_event",
    ]


async def test_decide_receives_neighbors_per_fact(req: AddRequest):
    """decide_actions step must be passed neighbors shaped as list-per-fact."""
    event_id = uuid4()
    ghost_uuid = uuid4()
    captured: dict[str, Any] = {}

    ctx = FakeContext(workflow_key=str(event_id))
    ctx.canned = {
        "create_event": None,
        "extract_facts": ["a", "b"],
        "knn:0": [{"memory_id": str(ghost_uuid), "content": "old fact", "distance": 0.1}],
        "knn:1": [],
        "decide_actions": [],
        "apply_actions": [],
        "finish_event": None,
    }

    # Patch the workflow's decide step so we can grab the neighbors it received.
    from prepr_mem0.workflow import _steps  # noqa: PLC0415

    orig = _steps.decide_actions_step

    async def _spy(facts, neighbors_per_fact):
        captured["facts"] = facts
        captured["neighbors"] = neighbors_per_fact
        return []

    _steps.decide_actions_step = _spy  # type: ignore[assignment]
    try:
        await run_add_memory(ctx, req)
    finally:
        _steps.decide_actions_step = orig  # type: ignore[assignment]

    assert captured["facts"] == ["a", "b"]
    # neighbors arrives shaped list[list[Neighbor]]: one inner list per fact.
    assert len(captured["neighbors"]) == 2
    assert isinstance(captured["neighbors"][0], list)
    assert isinstance(captured["neighbors"][1], list)
    # And the UUID round-trips back from the serialized form
    assert captured["neighbors"][0][0].memory_id == ghost_uuid


async def test_event_id_derived_from_workflow_key(req: AddRequest):
    target = UUID("11111111-1111-1111-1111-111111111111")
    ctx = FakeContext(
        workflow_key=str(target),
        canned={
            "create_event": None,
            "extract_facts": [],
            "decide_actions": [],
            "apply_actions": [],
            "finish_event": None,
        },
    )
    result = await run_add_memory(ctx, req)
    assert result.event_id == target
