"""Repo layer integration tests against the live tmpfs Postgres."""

from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy import select

from prepr_mem0.db.models import Memory, MemoryHistory
from prepr_mem0.db.repo import AppliedAction, DecidedAction, Repo
from prepr_mem0.embeddings import embed_text

pytestmark = pytest.mark.asyncio


async def test_apply_actions_add_writes_memory_and_history(session):
    repo = Repo(session)
    applied = await repo.apply_actions_tx(
        user_id="alice",
        actions=[
            DecidedAction(fact="alice loves hiking", event="ADD"),
            DecidedAction(fact="alice drives a tesla", event="ADD"),
        ],
    )
    assert len(applied) == 2
    assert {a.event for a in applied} == {"ADD"}

    mems = (await session.execute(select(Memory))).scalars().all()
    assert {m.content for m in mems} == {"alice loves hiking", "alice drives a tesla"}

    history = (await session.execute(select(MemoryHistory))).scalars().all()
    assert len(history) == 2
    assert all(h.event == "ADD" for h in history)


async def test_apply_actions_update_writes_old_and_new(session):
    repo = Repo(session)
    [first] = await repo.apply_actions_tx(
        "alice",
        [DecidedAction(fact="alice likes coffee", event="ADD")],
    )
    [second] = await repo.apply_actions_tx(
        "alice",
        [
            DecidedAction(
                fact="alice prefers tea",
                event="UPDATE",
                target_memory_id=first.memory_id,
            )
        ],
    )
    assert second.memory_id == first.memory_id
    assert second.event == "UPDATE"

    hist = await repo.history_for(first.memory_id)
    events = [h.event for h in hist]
    assert events == ["ADD", "UPDATE"]
    update_row = hist[1]
    assert update_row.old_memory == "alice likes coffee"
    assert update_row.new_memory == "alice prefers tea"


async def test_apply_actions_update_skips_when_content_unchanged(session):
    repo = Repo(session)
    [first] = await repo.apply_actions_tx(
        "alice",
        [DecidedAction(fact="same fact", event="ADD")],
    )
    [second] = await repo.apply_actions_tx(
        "alice",
        [
            DecidedAction(
                fact="same fact",
                event="UPDATE",
                target_memory_id=first.memory_id,
            )
        ],
    )
    assert second.event == "NONE", "identical content should short-circuit to NONE"
    hist = await repo.history_for(first.memory_id)
    assert [h.event for h in hist] == ["ADD"], "no UPDATE row written for no-op"


async def test_apply_actions_delete_soft_deletes_and_logs(session):
    repo = Repo(session)
    [first] = await repo.apply_actions_tx(
        "alice",
        [DecidedAction(fact="forget me", event="ADD")],
    )
    [second] = await repo.apply_actions_tx(
        "alice",
        [DecidedAction(fact="forget me", event="DELETE", target_memory_id=first.memory_id)],
    )
    assert second.event == "DELETE"
    visible = await repo.list_memories("alice")
    assert visible == [], "soft-deleted memory must not appear in default list"
    hist = await repo.history_for(first.memory_id)
    assert [h.event for h in hist] == ["ADD", "DELETE"]


async def test_knn_returns_self_at_distance_zero(session):
    repo = Repo(session)
    [first] = await repo.apply_actions_tx(
        "alice",
        [DecidedAction(fact="alice loves hiking", event="ADD")],
    )
    neighbors = await repo.knn("alice", "alice loves hiking", k=3)
    assert len(neighbors) >= 1
    assert neighbors[0].memory_id == first.memory_id
    assert neighbors[0].distance == pytest.approx(0.0, abs=1e-6)


async def test_knn_filters_by_user(session):
    repo = Repo(session)
    await repo.apply_actions_tx("alice", [DecidedAction(fact="apple", event="ADD")])
    await repo.apply_actions_tx("bob", [DecidedAction(fact="apple", event="ADD")])
    a = await repo.knn("alice", "apple", k=10)
    b = await repo.knn("bob", "apple", k=10)
    assert len(a) == 1
    assert len(b) == 1
    assert a[0].memory_id != b[0].memory_id


async def test_embedding_is_deterministic_and_unit_norm():
    v1 = embed_text("hello world")
    v2 = embed_text("hello world")
    assert v1 == v2
    norm = sum(x * x for x in v1) ** 0.5
    assert norm == pytest.approx(1.0, abs=1e-9)


async def test_create_event_then_finish_event_round_trip(session):
    repo = Repo(session)
    eid = uuid4()
    await repo.create_event(eid, "alice")
    row = await repo.get_event(eid)
    assert row is not None
    assert row.status == "PENDING"

    await repo.finish_event(
        eid,
        status="SUCCEEDED",
        result=[AppliedAction(memory_id=uuid4(), event="ADD", fact="x")],
        latency_ms=42,
    )
    row2 = await repo.get_event(eid)
    assert row2 is not None
    assert row2.status == "SUCCEEDED"
    assert row2.latency_ms == 42
    assert row2.result is not None
    assert row2.result[0]["event"] == "ADD"
