"""FastAPI app. Edge layer — owns no business logic, just routes + I/O.

POST /v1/memories enqueues the durable `add_memory` workflow (wired in Phase 5).
GET /v1/events/{event_id} polls workflow status from `add_events`.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status

from prepr_mem0 import __version__
from prepr_mem0.db import Repo
from prepr_mem0.db.engine import session_scope
from prepr_mem0.schemas import (
    AddRequest,
    AddResult,
    EventStatus,
    EventStatusResponse,
)
from prepr_mem0.schemas.api import AppliedAction

app = FastAPI(
    title="prepr-mem0",
    version=__version__,
    description="Durable Mem0-style memory API on Restate + FastAPI.",
)


async def _repo() -> AsyncIterator[Repo]:
    """Per-request repo. Caller-managed session, opened+closed per request."""
    async with session_scope() as session:
        yield Repo(session)


@app.get("/healthz")
async def healthz() -> dict[str, bool]:
    return {"ok": True}


@app.post(
    "/v1/memories",
    response_model=AddResult,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enqueue the add_memory durable workflow",
)
async def add_memories(req: AddRequest) -> AddResult:
    # Phase 5 will replace this with a Restate send-invoke. Until then, 501.
    _ = req
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="add_memory workflow not yet wired — see Phase 5",
    )


@app.get(
    "/v1/events/{event_id}",
    response_model=EventStatusResponse,
    summary="Poll the status of a previously enqueued add_memory event",
)
async def get_event(event_id: UUID, repo: Annotated[Repo, Depends(_repo)]) -> EventStatusResponse:
    row = await repo.get_event(event_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="event not found")
    return EventStatusResponse(
        event_id=row.id,
        user_id=row.user_id,
        status=EventStatus(row.status),
        latency_ms=row.latency_ms,
        error=row.error,
        result=(
            [AppliedAction.model_validate(item) for item in row.result]
            if row.result is not None
            else None
        ),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
