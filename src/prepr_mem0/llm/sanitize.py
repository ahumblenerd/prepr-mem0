"""Sanitize raw LLM output.

Ports of the helpers in `mem0/memory/utils.py`:

- `remove_code_blocks` strips a single ```lang ... ``` wrapper AND any
  `<think>...</think>` reasoning-model tags.
- `normalize_facts` accepts `["a", "b"]` or `[{"fact": "a"}]` or
  `[{"text": "b"}]`, returning a clean `list[str]`.
- `extract_json` pulls the JSON substring out of a markdown-wrapped or
  prose-padded LLM response.

Source attribution: https://github.com/mem0ai/mem0/blob/main/mem0/memory/utils.py
"""

from __future__ import annotations

import re
from typing import Any

_FENCE_RE = re.compile(r"^```[a-zA-Z0-9]*\n([\s\S]*?)\n```$")
_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def remove_code_blocks(content: str) -> str:
    """Strip a leading/trailing ``` fence + any <think>...</think> blocks."""
    stripped = content.strip()
    match = _FENCE_RE.match(stripped)
    inner = match.group(1).strip() if match else stripped
    return _THINK_RE.sub("", inner).strip()


def normalize_facts(raw_facts: list[Any] | None) -> list[str]:
    """Coerce the LLM's fact list into a clean list[str]."""
    if not raw_facts:
        return []
    out: list[str] = []
    for item in raw_facts:
        fact: str | None
        if isinstance(item, str):
            fact = item
        elif isinstance(item, dict):
            raw: object = item.get("fact") or item.get("text")  # type: ignore[reportUnknownMemberType]
            fact = raw if isinstance(raw, str) else None
        else:
            fact = str(item)
        if fact:
            out.append(fact)
    return out


def extract_json(text: str) -> str:
    """Locate the JSON payload inside an LLM response. Best-effort."""
    text = text.strip()
    fence = _JSON_FENCE_RE.search(text)
    if fence:
        return fence.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text
