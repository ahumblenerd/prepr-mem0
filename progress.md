# Progress

Live tracker for the build laid out in [PLAN.md](./PLAN.md). Each phase has a
**Verify** column re-runnable from a clean checkout.

| Phase | Status | One-line summary |
| ----- | ------ | ---------------- |
| 0 — Repo skeleton + quality gate | done | `just check` enforces ruff (`ALL`) + pyright strict + bandit + pytest |
| 1 — Postgres + pgvector in compose | done | `just up-db && just migrate && just db-smoke` brings up `pgvector/pg16` on tmpfs with the three-table schema |
| 2 — FastAPI skeleton + DB repo + deterministic embedder | done | 15 tests, 92.7% coverage; `GET /v1/events/{id}` real; `POST /v1/memories` is a 501 stub until Phase 5 |
| 3 — Restate runtime + echo workflow | done | `just up` composes pg + restate + worker + register; `curl :8080/memory/echo` round-trips through the runtime |
| 4 — OpenRouter wrapper + Mem0 prompts | done | `extract_facts` + `decide_actions` typed wrappers, prompts lifted verbatim, 25 respx-mocked tests, coverage 91% |
| 5 — Durable `add_memory` E2E | done | six-step `ctx.run` workflow registered with Restate; `POST /v1/memories` send-invokes it and returns PENDING; 47 tests, 93.7% coverage |
| 6 — Chaos test (the headline) | next | kill worker mid-extract; assert fake OpenRouter call count == 2 |

---

## Phase 0 — done

`uv`-managed project, ruff `select = ALL` with a curated ignore list (`D`,
`COM812`, `ISC001`, `FIX`, `TD`, `CPY`, `FBT`, `PLR0913`, `TC00*`, `B008`),
pyright strict on `src/` and basic on `tests/`, bandit excluding tests,
pytest with `asyncio_mode = auto`, session-scoped event loop for SQLAlchemy.
pre-commit installed. `just check` is the single quality gate.

Verified: `just check` exits 0 clean; planted violation makes it fail; revert
restores green.

## Phase 1 — done

`pgvector/pg16` on tmpfs (port 5433 to avoid clashing with any host pg).
`migrations/0001_init.sql` (idempotent) provisions `memories`, `memory_history`,
`add_events` with CHECK constraints, partial indexes for soft-delete, and an
`ivfflat` cosine index sized for a small dev table.

Verified: extensions present, all three tables present, 1536-d vector round-trips
through pgvector with cosine distance to self = 0.

## Phase 2 — done

Schemas (`Message`, `AddRequest`, `AddResult`, `EventStatus`, `FactAction`,
`AppliedAction`) in pydantic v2. SQLAlchemy 2.x async models matching the
migration. `Repo` exposes `create_event` / `finish_event` / `get_event`,
`knn`, `apply_actions_tx` (the atomic ADD/UPDATE/DELETE/NONE applier that
mirrors mem0's `_add_to_vector_store`), plus `list_memories` and
`history_for`. Deterministic SHA-256-seeded embedding stub — same text → same
1536-d unit vector. FastAPI app with `/healthz`, `GET /v1/events/{id}`, and
the `POST /v1/memories` 501 stub.

Tests use `ASGITransport` + the live tmpfs Postgres (no testcontainers spin-up
overhead). Session-scoped engine, per-test truncate. **15 tests, 92.7%
coverage** — well above the 80% floor.

Tuning notes:

- ruff `TC00*` + `B008` suppressed (wrong for SQLAlchemy `mapped_column` and
  FastAPI `Depends`).
- pyright relaxed on `tests/` only — pytest fixtures' untyped returns are not
  worth annotating around.
- Bandit `B324` md5 fixed properly with `usedforsecurity=False`; `B311` random
  has a justification comment for the deterministic-seed use case.

## Phase 3 — done

`docker.restate.dev/restatedev/restate:1.4` added to compose with ports 8080
(ingress), 9070 (admin), 9071. `src/prepr_mem0/workflow/echo.py` defines a
`memory.echo` handler; `workflow/asgi.py` exposes the ASGI app via
`restate.app([echo_service])`. `just up` composes everything: pg + restate +
migrations + worker + registration. `scripts/register_workflow.sh` POSTs to
the admin API with `use_http_11: true` and `force: true` so re-runs are
idempotent.

Verified manually: `curl -X POST :8080/memory/echo -d '"ping"'` returns
`"ping"`. No formal integration test for it — Phase 5's e2e test exercises
the same plumbing for real.

Snag worth flagging: Restate defaults to HTTP/2 for service discovery, and
uvicorn doesn't speak h2c without TLS. Fix: pass `use_http_11: true` in the
deployment payload. Standard pitfall.

---

## Phase 4 — done

`src/prepr_mem0/llm/` has the two typed entry points the workflow will call:

- `extract_facts(messages, agent_id=None) -> list[str]` runs Mem0's
  `USER_MEMORY_EXTRACTION_PROMPT` (or `AGENT_MEMORY_EXTRACTION_PROMPT` when
  `agent_id` is set), in `response_format=json_object` mode, through the
  `openai` async SDK pointed at `openrouter.ai/api/v1`.
- `decide_actions(facts, neighbors_per_fact) -> list[DecidedAction]` runs
  Mem0's `update_memory_template`. UUIDs are remapped to small string ids
  (`"0","1",...`) before they hit the LLM and mapped back on response;
  unknown ids the LLM hallucinates are dropped, not crashed on.

Sanitization (`sanitize.py`) lifts Mem0's `remove_code_blocks` /
`normalize_facts` / `extract_json` — strips ``` fences, strips
`<think>...</think>` reasoning blocks, accepts `{"fact": "x"}` or bare
strings, recovers JSON from prose-padded output.

Prompts in `prompts.py` are verbatim from `mem0/configs/prompts.py` (cited
in the module docstring). Per-file ruff E501 ignore lets them stay
unbroken.

Tests: 25 new ones in `tests/unit/llm/` (12 sanitize + 7 extract + 6
decide), all respx-mocked at the httpx transport. Coverage 91.5% (floor
bumped to 85%). `openai` SDK's built-in `max_retries=3` covers the 429
case — verified by the side-effect-sequence test.

## Phase 5 — done

`src/prepr_mem0/workflow/add_memory.py` defines a `restate.Workflow`
keyed by `event_id`. The workflow body is a pure function
`run_add_memory(ctx, req)` that takes a duck-typed `ctx` so unit tests
can drive it with a `FakeContext`. Six journaled steps in order:

    create_event -> extract_facts -> knn:0..N -> decide_actions
    -> apply_actions -> finish_event

Each step lives in `_steps.py` as a thin wrapper that opens its own
`session_scope()` and returns JSON-friendly values (dicts of strings,
not dataclasses or UUIDs) so Restate's default serde can journal them.
The workflow body converts back to `Neighbor` / `DecidedAction` at the
boundary.

The Restate registration response now lists both `memory.echo` and
`add_memory.run`. `POST /v1/memories` was rewritten to `generic_send`
into Restate ingress and return `{event_id, status: PENDING}`; the
generated `event_id` becomes the workflow key.

Tests:

- 4 unit tests in `tests/unit/workflow/test_add_orders_steps.py` with
  a `FakeContext` that records `ctx.run` calls. Asserts step order, the
  per-fact `knn:i` naming, and that `decide_actions` receives neighbors
  shaped `list[list[Neighbor]]`.
- 3 integration tests in `tests/integration/test_workflow.py` running
  the workflow body against the real Postgres with respx-mocked
  OpenRouter. Covers the happy path (two ADDs end up in memories +
  history + event row), reconciliation (NONE leaves the seeded row
  alone), and apply-failure (event stays PENDING, no memories written).

Skipped: a real-Restate-process e2e test. respx is process-local and
can't mock httpx in the worker subprocess. Phase 6's fake_openrouter
HTTP server is the right tool for that — it'll be reused as the durable
call counter for the chaos test.

Snag worth flagging: Restate's Python client speaks HTTP/2 to the
ingress, so `httpx[http2]` (which pulls in `h2`) had to go into the
project dependencies. Without it, `restate_client()` raises an
ImportError at first connect.

## Next session

Open Phase 6 — the chaos test.

Build order:

1. `tests/chaos/fake_openrouter.py` — a tiny FastAPI app on :9999 that
   serves canned `/chat/completions` responses and appends each request
   to `/tmp/openrouter_calls.jsonl`. The file is the durable call
   counter across worker restarts.
2. `src/prepr_mem0/workflow/chaos.py` — `maybe_crash(hook)` that calls
   `os._exit(1)` when `CHAOS_AT=$hook` is set. Wire one call into the
   workflow body right after `extract_facts` completes.
3. `tests/chaos/test_resume_after_crash.py` — wipe the jsonl, start
   the fake server, restart the worker with `CHAOS_AT=after_extract_facts`
   and `OPENROUTER_BASE_URL=http://host.docker.internal:9999`, POST,
   wait for crash, restart worker without `CHAOS_AT`, poll until
   SUCCEEDED, assert the jsonl line count is exactly 2.
4. `just chaos` target + `scripts/chaos.sh` wrapper.
5. Bump coverage floor / re-verify.
