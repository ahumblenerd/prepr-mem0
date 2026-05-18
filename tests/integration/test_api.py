"""FastAPI app integration tests via httpx ASGITransport (no network)."""

from __future__ import annotations

from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from prepr_mem0.api import app
from prepr_mem0.db.repo import AppliedAction, Repo

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def test_healthz(client):
    r = await client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"ok": True}


async def test_openapi_lists_v1_paths(client):
    r = await client.get("/openapi.json")
    assert r.status_code == 200
    paths = set(r.json()["paths"].keys())
    assert "/v1/memories" in paths
    assert "/v1/events/{event_id}" in paths


async def test_add_memories_returns_501_stub(client):
    r = await client.post(
        "/v1/memories",
        json={"user_id": "alice", "messages": [{"role": "user", "content": "hi"}]},
    )
    assert r.status_code == 501


async def test_add_memories_validates_payload(client):
    r = await client.post("/v1/memories", json={"messages": []})
    assert r.status_code == 422


async def test_event_endpoint_404_unknown_event(client):
    r = await client.get(f"/v1/events/{uuid4()}")
    assert r.status_code == 404


async def test_event_endpoint_returns_finished_event(client, session):
    repo = Repo(session)
    eid = uuid4()
    await repo.create_event(eid, "alice")
    await repo.finish_event(
        eid,
        status="SUCCEEDED",
        result=[AppliedAction(memory_id=uuid4(), event="ADD", fact="x")],
        latency_ms=10,
    )
    r = await client.get(f"/v1/events/{eid}")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "SUCCEEDED"
    assert body["latency_ms"] == 10
    assert body["result"][0]["event"] == "ADD"
