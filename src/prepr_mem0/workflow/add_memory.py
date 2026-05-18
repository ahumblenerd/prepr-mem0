"""Durable `add_memory` workflow.

Six-step pipeline keyed by `event_id`:

    create_event -> extract_facts -> knn:0..N -> decide_actions
    -> apply_actions -> finish_event

Every step is a `ctx.run(...)` so Restate journals the return value. On
crash + replay, completed steps return their cached results instead of
re-executing — the LLM is never billed twice for the same `event_id`.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

import restate

from prepr_mem0.db.repo import Neighbor
from prepr_mem0.schemas.api import AddRequest, AddResult
from prepr_mem0.workflow import _steps


def _neighbor_from_dict(d: dict[str, Any]) -> Neighbor:
    return Neighbor(
        memory_id=UUID(d["memory_id"]),
        content=d["content"],
        distance=float(d["distance"]),
    )


async def run_add_memory(ctx: Any, req: AddRequest) -> AddResult:  # noqa: ANN401
    """The workflow body. Duck-typed `ctx` so unit tests can pass a fake."""
    event_id = UUID(ctx.key())
    started = _steps.now_ms()

    await ctx.run("create_event", lambda: _steps.create_event_step(event_id, req.user_id))

    facts: list[str] = await ctx.run(
        "extract_facts",
        lambda: _steps.extract_facts_step(req.messages, req.agent_id),
    )

    neighbors_per_fact: list[list[Neighbor]] = []
    for i, fact in enumerate(facts):
        raw = await ctx.run(f"knn:{i}", lambda f=fact: _steps.knn_step(req.user_id, f))
        neighbors_per_fact.append([_neighbor_from_dict(d) for d in raw])

    actions_payload: list[dict[str, Any]] = await ctx.run(
        "decide_actions",
        lambda: _steps.decide_actions_step(facts, neighbors_per_fact),
    )

    applied: list[dict[str, Any]] = await ctx.run(
        "apply_actions",
        lambda: _steps.apply_actions_step(req.user_id, actions_payload, req.agent_id, req.run_id),
    )

    await ctx.run(
        "finish_event",
        lambda: _steps.finish_event_step(event_id, applied, "SUCCEEDED", started),
    )

    return AddResult(event_id=event_id, status="SUCCEEDED")


add_memory_wf = restate.Workflow("add_memory")


@add_memory_wf.main()
async def run(ctx: restate.WorkflowContext, req: AddRequest) -> AddResult:
    return await run_add_memory(ctx, req)
