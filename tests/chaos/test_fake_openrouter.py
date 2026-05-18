"""Smoke test for the fake OpenRouter server."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.fixture
def calls_path(tmp_path, monkeypatch):
    path = tmp_path / "calls.jsonl"
    monkeypatch.setenv("FAKE_OPENROUTER_LOG", str(path))
    yield path
    if path.exists():
        path.unlink()


@pytest.fixture
async def fake_client(calls_path):
    # Reload so the freshly-set env var is picked up.
    import importlib

    from tests.chaos import fake_openrouter as fake  # pyright: ignore[reportMissingImports]

    importlib.reload(fake)
    assert os.environ["FAKE_OPENROUTER_LOG"] == str(calls_path)
    transport = ASGITransport(app=fake.app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def test_records_each_call_to_jsonl(fake_client, calls_path: Path):
    r = await fake_client.post(
        "/chat/completions",
        json={"messages": [{"role": "user", "content": "Personal Information Organizer hint"}]},
    )
    assert r.status_code == 200
    body = r.json()
    assert "Name is Alice" in body["choices"][0]["message"]["content"]

    lines = calls_path.read_text().strip().splitlines()
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["path"] == "/chat/completions"


async def test_returns_decide_shape_on_second_request(fake_client):
    r = await fake_client.post(
        "/chat/completions",
        json={"messages": [{"role": "user", "content": "memory manager prompt"}]},
    )
    body = r.json()
    payload = json.loads(body["choices"][0]["message"]["content"])
    assert "memory" in payload
    assert payload["memory"][0]["event"] == "ADD"
