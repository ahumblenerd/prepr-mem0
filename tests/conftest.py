"""Shared fixtures.

Integration tests share the running compose Postgres (the tmpfs one). No
testcontainers spin-up: faster inner loop, single source of truth for schema.
Tests are responsible for truncating tables they touch.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from prepr_mem0.config import Settings


@pytest.fixture(scope="session")
def db_url() -> str:
    return Settings.from_env().database_url


@pytest.fixture(scope="session")
async def engine(db_url: str):
    eng = create_async_engine(db_url, pool_pre_ping=True)
    try:
        yield eng
    finally:
        await eng.dispose()


@pytest.fixture
async def session(engine) -> AsyncIterator[AsyncSession]:
    sm = async_sessionmaker(engine, expire_on_commit=False)
    async with sm() as s:
        # Truncate before each test for isolation. Keep this list in sync with migrations.
        await s.execute(
            text("TRUNCATE memories, memory_history, add_events RESTART IDENTITY CASCADE")
        )
        await s.commit()
        yield s
