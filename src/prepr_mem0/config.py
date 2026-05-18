"""Runtime configuration. Reads from env, with sane dev defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    openrouter_api_key: str
    openrouter_model: str
    openrouter_base_url: str
    restate_ingress_url: str

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            database_url=os.environ.get(
                "DATABASE_URL",
                "postgresql+asyncpg://prepr:prepr@localhost:5433/prepr",
            ),
            openrouter_api_key=os.environ.get("OPENROUTER_API_KEY", ""),
            openrouter_model=os.environ.get(
                "OPENROUTER_MODEL",
                "openrouter/anthropic/claude-haiku-4-5",
            ),
            openrouter_base_url=os.environ.get(
                "OPENROUTER_BASE_URL",
                "https://openrouter.ai/api/v1",
            ),
            restate_ingress_url=os.environ.get(
                "RESTATE_INGRESS_URL",
                "http://localhost:8080",
            ),
        )
