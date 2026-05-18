"""Public request/response schemas. Pydantic v2."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class MessageRole(StrEnum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    role: MessageRole
    content: str


class AddRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=200)
    agent_id: str | None = Field(default=None, max_length=200)
    run_id: str | None = Field(default=None, max_length=200)
    messages: list[Message] = Field(min_length=1)


class AppliedAction(BaseModel):
    memory_id: UUID
    event: str  # ADD | UPDATE | DELETE | NONE
    fact: str


class AddResult(BaseModel):
    event_id: UUID
    status: str  # PENDING on the initial response, terminal value on poll


class EventStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class EventStatusResponse(BaseModel):
    event_id: UUID
    user_id: str
    status: EventStatus
    latency_ms: int | None
    error: str | None
    result: list[AppliedAction] | None
    created_at: datetime
    updated_at: datetime


class FactAction(BaseModel):
    """One LLM-decided action: ADD / UPDATE / DELETE / NONE for a fact."""

    fact: str
    event: str  # ADD | UPDATE | DELETE | NONE
    target_memory_id: UUID | None = None  # set only for UPDATE / DELETE
    metadata: dict[str, Any] = Field(default_factory=dict)
