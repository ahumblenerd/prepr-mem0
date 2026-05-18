"""Side-effect steps for the add_memory workflow.

Each function opens a fresh DB session, does its thing, returns a
JSON-serializable value, and closes. They are designed to be the body of
a `ctx.run("name", ...)` call — Restate journals the return value, so
replay returns the cached value without re-executing the step.

Steps take and return primitives / lists of dicts so the journal
serializer doesn't have to know about dataclasses or UUIDs. The workflow
body converts at the boundary.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from prepr_mem0.db import Repo
from prepr_mem0.db.engine import session_scope
from prepr_mem0.db.repo import DecidedAction, Neighbor
from prepr_mem0.llm.decide import decide_actions
from prepr_mem0.llm.extract import extract_facts
from prepr_mem0.schemas.api import Message


async def create_event_step(event_id: UUID, user_id: str) -> None:
    async with session_scope() as session:
        await Repo(session).create_event(event_id, user_id)


async def extract_facts_step(messages: list[Message], agent_id: str | None) -> list[str]:
    return await extract_facts(messages, agent_id=agent_id)


async def knn_step(user_id: str, fact: str, k: int = 5) -> list[dict[str, Any]]:
    async with session_scope() as session:
        neighbors = await Repo(session).knn(user_id, fact, k=k)
    return [
        {"memory_id": str(n.memory_id), "content": n.content, "distance": n.distance}
        for n in neighbors
    ]


async def decide_actions_step(
    facts: list[str],
    neighbors_per_fact: list[list[Neighbor]],
) -> list[dict[str, Any]]:
    actions = await decide_actions(facts, neighbors_per_fact)
    return [
        {
            "fact": a.fact,
            "event": a.event,
            "target_memory_id": str(a.target_memory_id) if a.target_memory_id else None,
        }
        for a in actions
    ]


async def apply_actions_step(
    user_id: str,
    actions_payload: list[dict[str, Any]],
    agent_id: str | None,
    run_id: str | None,
) -> list[dict[str, Any]]:
    actions = [
        DecidedAction(
            fact=a["fact"],
            event=a["event"],
            target_memory_id=UUID(a["target_memory_id"]) if a.get("target_memory_id") else None,
        )
        for a in actions_payload
    ]
    async with session_scope() as session:
        applied = await Repo(session).apply_actions_tx(
            user_id,
            actions,
            agent_id=agent_id,
            run_id=run_id,
        )
    return [{"memory_id": str(a.memory_id), "event": a.event, "fact": a.fact} for a in applied]


async def finish_event_step(
    event_id: UUID,
    applied: list[dict[str, Any]],
    status: str,
    started_ms: int,
    error: str | None = None,
) -> None:
    from prepr_mem0.db.repo import AppliedAction as RepoAppliedAction  # noqa: PLC0415

    latency = int(datetime.now(UTC).timestamp() * 1000) - started_ms
    async with session_scope() as session:
        await Repo(session).finish_event(
            event_id,
            status=status,  # type: ignore[arg-type]
            result=[
                RepoAppliedAction(
                    memory_id=UUID(a["memory_id"]),
                    event=a["event"],  # type: ignore[arg-type]
                    fact=a["fact"],
                )
                for a in applied
            ]
            if status == "SUCCEEDED"
            else None,
            error=error,
            latency_ms=latency,
        )


def now_ms() -> int:
    return int(time.time() * 1000)
