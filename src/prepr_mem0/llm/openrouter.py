"""Shared async OpenRouter client.

OpenRouter speaks the OpenAI Chat Completions wire format, so we use the
official `openai` SDK with a `base_url` override. The SDK runs on httpx
under the hood, which is what makes respx interception work in tests.
"""

from __future__ import annotations

from openai import AsyncOpenAI

from prepr_mem0.config import Settings

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    """Return a process-wide AsyncOpenAI client bound to OpenRouter."""
    global _client  # noqa: PLW0603 — module-level singleton is the point
    if _client is None:
        settings = Settings.from_env()
        _client = AsyncOpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key or "test",
            max_retries=3,
        )
    return _client


def reset_client_for_tests() -> None:
    """Drop the cached client so a new env / base_url takes effect."""
    global _client  # noqa: PLW0603
    _client = None
