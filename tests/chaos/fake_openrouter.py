"""Tiny FastAPI app that impersonates OpenRouter's chat completions API.

Each request is appended to `/tmp/openrouter_calls.jsonl`. That file is
the durable call counter that survives the worker process being killed
and restarted — respx couldn't do this because it's process-local.

Run standalone: `uv run uvicorn tests.chaos.fake_openrouter:app --port 9999`.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request

app = FastAPI()

CALLS_PATH = Path(os.environ.get("FAKE_OPENROUTER_LOG", "/tmp/openrouter_calls.jsonl"))  # noqa: S108


def _completion(content: str) -> dict[str, Any]:
    return {
        "id": "fake",
        "object": "chat.completion",
        "created": 0,
        "model": "fake",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            },
        ],
    }


def _looks_like_extract(body_text: str) -> bool:
    return "Personal Information Organizer" in body_text or '"facts"' in body_text.lower()


@app.post("/chat/completions")
async def chat_completions(request: Request) -> dict[str, Any]:
    raw = await request.body()
    record = {
        "path": "/chat/completions",
        "body": raw.decode("utf-8", errors="replace"),
    }
    with CALLS_PATH.open("a") as f:
        f.write(json.dumps(record) + "\n")

    if _looks_like_extract(record["body"]):
        return _completion(json.dumps({"facts": ["Name is Alice", "Likes tea"]}))
    return _completion(
        json.dumps(
            {
                "memory": [
                    {"id": "0", "text": "Name is Alice", "event": "ADD"},
                    {"id": "1", "text": "Likes tea", "event": "ADD"},
                ]
            }
        )
    )


@app.get("/healthz")
async def healthz() -> dict[str, bool]:
    return {"ok": True}
