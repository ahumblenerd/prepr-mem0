"""LLM action decider. Second of Mem0's two calls in `Memory.add()`.

Maps existing memory UUIDs to small string ids ("0","1",...) before they hit
the LLM, then maps the response ids back. This is Mem0's trick to keep small
models from hallucinating UUIDs.
"""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from prepr_mem0.config import Settings
from prepr_mem0.db.repo import DecidedAction, Neighbor
from prepr_mem0.llm.openrouter import get_client
from prepr_mem0.llm.prompts import build_update_memory_messages
from prepr_mem0.llm.sanitize import extract_json, remove_code_blocks

_VALID_EVENTS: set[str] = {"ADD", "UPDATE", "DELETE", "NONE"}


def _build_id_remap(
    neighbors_per_fact: list[list[Neighbor]],
) -> tuple[dict[str, UUID], list[dict[str, str]]]:
    """Map each unique neighbor UUID to a small string id ("0","1",...)."""
    int_to_uuid: dict[str, UUID] = {}
    old_memory: list[dict[str, str]] = []
    seen: set[UUID] = set()
    for nlist in neighbors_per_fact:
        for n in nlist:
            if n.memory_id in seen:
                continue
            seen.add(n.memory_id)
            idx = str(len(int_to_uuid))
            int_to_uuid[idx] = n.memory_id
            old_memory.append({"id": idx, "text": n.content})
    return int_to_uuid, old_memory


def _parse_entry(
    entry: dict[str, Any],
    int_to_uuid: dict[str, UUID],
) -> DecidedAction | None:
    event = entry.get("event")
    text = entry.get("text")
    if event not in _VALID_EVENTS or not isinstance(text, str):
        return None
    if event == "ADD":
        return DecidedAction(fact=text, event="ADD", target_memory_id=None)
    target = int_to_uuid.get(str(entry.get("id")))
    if target is None:
        return None
    return DecidedAction(fact=text, event=event, target_memory_id=target)


async def decide_actions(
    facts: list[str],
    neighbors_per_fact: list[list[Neighbor]],
) -> list[DecidedAction]:
    """Call the LLM with remapped ids and return decoded actions."""
    if not facts:
        return []

    int_to_uuid, old_memory = _build_id_remap(neighbors_per_fact)
    user_prompt = build_update_memory_messages(old_memory, facts)

    client = get_client()
    settings = Settings.from_env()
    completion = await client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[
            {"role": "system", "content": "You are a careful memory manager."},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    raw = completion.choices[0].message.content or ""
    payload: dict[str, Any] = json.loads(extract_json(remove_code_blocks(raw)))

    actions: list[DecidedAction] = []
    entries: list[Any] = payload.get("memory") or []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        entry_typed: dict[str, Any] = entry  # type: ignore[reportUnknownVariableType]
        action = _parse_entry(entry_typed, int_to_uuid)
        if action is not None:
            actions.append(action)
    return actions
