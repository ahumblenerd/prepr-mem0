# Progress

Live tracker for the build laid out in [PLAN.md](./PLAN.md). Each phase has a
**Verify** column re-runnable from a clean checkout.

| Phase | Status | One-line summary |
| ----- | ------ | ---------------- |
| 0 — Repo skeleton + quality gate | done | `just check` enforces ruff (`ALL`) + pyright strict + bandit + pytest |
| 1 — Postgres + pgvector in compose | done | `just up-db && just migrate && just db-smoke` brings up `pgvector/pg16` on tmpfs with the three-table schema |
| 2 — FastAPI skeleton + DB repo + deterministic embedder | done | 15 tests, 92.7% coverage; `GET /v1/events/{id}` real; `POST /v1/memories` is a 501 stub until Phase 5 |
| 3 — Restate runtime + echo workflow | done | `just up` composes pg + restate + worker + register; `curl :8080/memory/echo` round-trips through the runtime |
| 4 — OpenRouter wrapper + Mem0 prompts | next | lift `USER_MEMORY_EXTRACTION_PROMPT` + `update_memory_template`; respx-mocked unit tests |
| 5 — Durable `add_memory` E2E | pending | the six-step `ctx.run` workflow in ARCH §6; `POST /v1/memories` send-invokes it |
| 6 — Chaos test (the headline) | pending | kill worker mid-extract; assert respx OpenRouter call count == 1 |

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

## Next session

Open Phase 4 — the OpenRouter wrapper. The first failing tests to write
(`tests/unit/llm/`):

1. `test_extract_facts.py::test_parses_clean_json_response`
2. `test_extract_facts.py::test_strips_markdown_fences`
3. `test_extract_facts.py::test_strips_think_tags`
4. `test_extract_facts.py::test_retries_on_429`
5. `test_decide_actions.py::test_remaps_uuids_to_small_ints`
6. `test_decide_actions.py::test_remaps_response_back_to_uuids`

Then implementation in `src/prepr_mem0/llm/` with `openrouter.py`,
`prompts.py` (lifted with attribution from `mem0/configs/prompts.py`),
`sanitize.py` (fence + `<think>` strip, fact normalization), `extract.py`,
`decide.py`. The chaos demo in Phase 6 depends on these calls being
respx-mockable, which they are by virtue of going through `httpx`.
