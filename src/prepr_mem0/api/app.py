"""FastAPI app. Edge layer — owns no business logic, just routes + I/O.

POST /v1/memories enqueues the durable `add_memory` workflow (wired in Phase 5).
GET /v1/events/{event_id} polls workflow status from `add_events`.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID, uuid4

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
from prepr_mem0.workflow.client import restate_client

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
    """Send-invoke the durable workflow keyed by a fresh event_id."""
    event_id = uuid4()
    payload = req.model_dump_json().encode("utf-8")
    async with restate_client() as client:
        await client.generic_send(
            service="add_memory",
            handler="run",
            arg=payload,
            key=str(event_id),
        )
    return AddResult(event_id=event_id, status="PENDING")


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
