"""Engine + sessionmaker singletons. FastAPI/Restate handlers inject from here."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from prepr_mem0.config import Settings


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    settings = Settings.from_env()
    return create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
    )


@lru_cache(maxsize=1)
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        get_engine(),
        expire_on_commit=False,
        autoflush=False,
    )


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession]:
    sm = get_sessionmaker()
    async with sm() as session:
        yield session
