"""LLM fact extraction. First of Mem0's two calls in `Memory.add()`."""

from __future__ import annotations

import json
from typing import Any

from prepr_mem0.config import Settings
from prepr_mem0.llm.openrouter import get_client
from prepr_mem0.llm.prompts import (
    AGENT_MEMORY_EXTRACTION_PROMPT,
    USER_MEMORY_EXTRACTION_PROMPT,
    format_transcript,
)
from prepr_mem0.llm.sanitize import extract_json, normalize_facts, remove_code_blocks
from prepr_mem0.schemas.api import Message


async def extract_facts(
    messages: list[Message],
    agent_id: str | None = None,
) -> list[str]:
    """Return the LLM-extracted facts as a clean list of strings."""
    system_prompt = AGENT_MEMORY_EXTRACTION_PROMPT if agent_id else USER_MEMORY_EXTRACTION_PROMPT
    transcript = format_transcript([{"role": m.role.value, "content": m.content} for m in messages])
    user_prompt = f"Input:\n{transcript}"

    client = get_client()
    settings = Settings.from_env()
    completion = await client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    raw = completion.choices[0].message.content or ""
    cleaned = remove_code_blocks(raw)
    payload_text = extract_json(cleaned)
    payload: dict[str, Any] = json.loads(payload_text)
    return normalize_facts(payload.get("facts") or [])
