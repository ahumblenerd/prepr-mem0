"""Repository layer.

Every function takes an `AsyncSession`. The caller owns the transaction
boundary. `apply_actions_tx` is the exception — it explicitly wraps a
single transaction because atomicity across `memories` + `memory_history`
is part of the contract (Mem0's `_add_to_vector_store` does the same).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from prepr_mem0.db.models import AddEvent, Memory, MemoryHistory
from prepr_mem0.embeddings import embed_text

Event = Literal["ADD", "UPDATE", "DELETE", "NONE"]


@dataclass(frozen=True)
class Neighbor:
    memory_id: UUID
    content: str
    distance: float


@dataclass(frozen=True)
class DecidedAction:
    fact: str
    event: Event
    target_memory_id: UUID | None = None


@dataclass(frozen=True)
class AppliedAction:
    memory_id: UUID
    event: Event
    fact: str


class Repo:
    """Thin wrapper that holds the session and exposes typed operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ---- events --------------------------------------------------------------

    async def create_event(self, event_id: UUID, user_id: str) -> None:
        self.session.add(AddEvent(id=event_id, user_id=user_id, status="PENDING"))
        await self.session.commit()

    async def set_event_status(self, event_id: UUID, status: str) -> None:
        await self.session.execute(
            update(AddEvent)
            .where(AddEvent.id == event_id)
            .values(status=status, updated_at=datetime.now(UTC)),
        )
        await self.session.commit()

    async def finish_event(
        self,
        event_id: UUID,
        *,
        status: Literal["SUCCEEDED", "FAILED"],
        result: list[AppliedAction] | None = None,
        error: str | None = None,
        latency_ms: int | None = None,
    ) -> None:
        await self.session.execute(
            update(AddEvent)
            .where(AddEvent.id == event_id)
            .values(
                status=status,
                result=(
                    [
                        {"memory_id": str(a.memory_id), "event": a.event, "fact": a.fact}
                        for a in result
                    ]
                    if result is not None
                    else None
                ),
                error=error,
                latency_ms=latency_ms,
                updated_at=datetime.now(UTC),
            ),
        )
        await self.session.commit()

    async def get_event(self, event_id: UUID) -> AddEvent | None:
        return await self.session.get(AddEvent, event_id)

    # ---- vector neighbors ----------------------------------------------------

    async def knn(
        self,
        user_id: str,
        text_query: str,
        *,
        k: int = 5,
    ) -> list[Neighbor]:
        emb = embed_text(text_query)
        sql = (
            select(
                Memory.id,
                Memory.content,
                Memory.embedding.cosine_distance(emb).label("distance"),
            )
            .where(Memory.user_id == user_id, Memory.deleted_at.is_(None))
            .order_by("distance")
            .limit(k)
        )
        rows = await self.session.execute(sql)
        return [
            Neighbor(memory_id=r.id, content=r.content, distance=float(r.distance)) for r in rows
        ]

    # ---- mutating ops --------------------------------------------------------

    async def apply_actions_tx(
        self,
        user_id: str,
        actions: list[DecidedAction],
        *,
        agent_id: str | None = None,
        run_id: str | None = None,
    ) -> list[AppliedAction]:
        """Apply ADD/UPDATE/DELETE/NONE atomically against memories + history.

        Idempotency note: the workflow journal keys this call by event_id, so
        Restate replays return the already-committed result without re-running.
        Within this function we do NOT dedupe — that's the journal's job.
        """
        applied: list[AppliedAction] = []
        for action in actions:
            if action.event == "ADD":
                mem = Memory(
                    user_id=user_id,
                    agent_id=agent_id,
                    run_id=run_id,
                    content=action.fact,
                    content_hash=_md5(action.fact),
                    embedding=embed_text(action.fact),
                )
                self.session.add(mem)
                await self.session.flush()
                self.session.add(
                    MemoryHistory(memory_id=mem.id, new_memory=action.fact, event="ADD"),
                )
                applied.append(AppliedAction(memory_id=mem.id, event="ADD", fact=action.fact))

            elif action.event == "UPDATE":
                if action.target_memory_id is None:
                    msg = "UPDATE action missing target_memory_id"
                    raise ValueError(msg)
                existing = await self.session.get(Memory, action.target_memory_id)
                if existing is None or existing.deleted_at is not None:
                    continue
                old = existing.content
                new_hash = _md5(action.fact)
                if existing.content_hash == new_hash:  # mem0 parity: skip redundant updates
                    applied.append(
                        AppliedAction(
                            memory_id=existing.id,
                            event="NONE",
                            fact=action.fact,
                        ),
                    )
                    continue
                existing.content = action.fact
                existing.content_hash = new_hash
                existing.embedding = embed_text(action.fact)
                existing.updated_at = datetime.now(UTC)
                self.session.add(
                    MemoryHistory(
                        memory_id=existing.id,
                        old_memory=old,
                        new_memory=action.fact,
                        event="UPDATE",
                    ),
                )
                applied.append(
                    AppliedAction(memory_id=existing.id, event="UPDATE", fact=action.fact),
                )

            elif action.event == "DELETE":
                if action.target_memory_id is None:
                    msg = "DELETE action missing target_memory_id"
                    raise ValueError(msg)
                existing = await self.session.get(Memory, action.target_memory_id)
                if existing is None or existing.deleted_at is not None:
                    continue
                existing.deleted_at = datetime.now(UTC)
                self.session.add(
                    MemoryHistory(
                        memory_id=existing.id,
                        old_memory=existing.content,
                        event="DELETE",
                    ),
                )
                applied.append(
                    AppliedAction(
                        memory_id=existing.id,
                        event="DELETE",
                        fact=action.fact,
                    ),
                )

            else:  # NONE
                applied.append(
                    AppliedAction(
                        memory_id=action.target_memory_id or _zero_uuid(),
                        event="NONE",
                        fact=action.fact,
                    ),
                )

        await self.session.commit()
        return applied

    # ---- reads (handy for verification + future search endpoint) -------------

    async def list_memories(
        self,
        user_id: str,
        *,
        include_deleted: bool = False,
    ) -> list[Memory]:
        stmt = select(Memory).where(Memory.user_id == user_id).order_by(Memory.created_at)
        if not include_deleted:
            stmt = stmt.where(Memory.deleted_at.is_(None))
        rows = await self.session.execute(stmt)
        return list(rows.scalars())

    async def history_for(self, memory_id: UUID) -> list[MemoryHistory]:
        rows = await self.session.execute(
            select(MemoryHistory)
            .where(MemoryHistory.memory_id == memory_id)
            .order_by(MemoryHistory.created_at),
        )
        return list(rows.scalars())


def _md5(s: str) -> str:
    # Content fingerprint, not security. mem0 uses md5 here for the same reason.
    return hashlib.md5(s.encode("utf-8"), usedforsecurity=False).hexdigest()


def _zero_uuid() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000000")
