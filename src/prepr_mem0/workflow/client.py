"""Restate ingress client used by FastAPI to enqueue workflow runs."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import restate

from prepr_mem0.config import Settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from restate.client_types import RestateClient


@asynccontextmanager
async def restate_client() -> AsyncGenerator[RestateClient]:
    """Yield a fresh `RestateClient` bound to the configured ingress URL."""
    settings = Settings.from_env()
    async with restate.create_client(settings.restate_ingress_url) as client:
        yield client
