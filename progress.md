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
| 6 — Chaos test (the headline) | wip | code + 5 supporting tests green; kill-and-replay run blocked on Docker — see Phase 6 note |

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

## Phase 6 — wip (code complete, end-to-end run not yet green)

All the code is written:

- `src/prepr_mem0/workflow/chaos.py` — `maybe_crash(hook)` that
  `os._exit(1)`s when `CHAOS_AT==hook`. Bypasses `sys.exit`'s
  `SystemExit` (the Restate SDK would otherwise catch it and turn the
  workflow into a `FAILED` status, defeating the test).
- `src/prepr_mem0/workflow/add_memory.py` plants
  `maybe_crash("after_extract_facts")` right after the extract step.
- `tests/chaos/fake_openrouter.py` — tiny FastAPI app on :9999 serving
  canned `/chat/completions` JSON and appending each request to
  `/tmp/openrouter_calls.jsonl`. Survives the worker dying, so it's the
  durable call counter the test asserts against.
- `tests/chaos/test_resume_after_crash.py` — orchestrates the kill /
  restart / poll, marked `@pytest.mark.chaos` so it's excluded from
  `just check`.
- `scripts/chaos.sh` + `just chaos` target.

**Supporting tests green** (`just check` runs them since they're
unmarked):

- `tests/chaos/test_chaos_hook.py` — 3 tests, each spawns a subprocess
  and asserts the exit code (1 when env set, 0 otherwise, 0 on hook
  name mismatch).
- `tests/chaos/test_fake_openrouter.py` — 2 tests, verify the server
  records each call to the configured jsonl path and returns
  extract-shaped vs decide-shaped responses correctly.

Total: 52 tests green, 1 chaos test deselected, 93.3% coverage.

**Snags fixed during the attempt:**

1. `generic_send` defaulted to `application/octet-stream` because
   `BytesSerde` doesn't set a content-type. Restate's workflow
   declares `application/json` input, so it rejected with 400. Fix:
   pass `headers={"content-type": "application/json"}` to
   `generic_send` in `api/app.py`.
2. `kill-api` / `kill-worker` trusted the `.pid` file blindly — if the
   pid was stale, the old uvicorn kept the port, and the new one
   silently failed to bind. Fix: both kill recipes now also
   `lsof -ti:<port> | xargs kill -9` to free the port.
3. `ctx.run("step", lambda: async_fn(...))` failed inside the worker
   with `TypeError: Object of type coroutine is not JSON serializable`.
   The Restate SDK checks `inspect.iscoroutinefunction(action)` — that
   returns `False` for a bare lambda even when the lambda returns a
   coroutine, so the SDK tried to JSON-encode the coroutine object.
   Fix: rewrite every `ctx.run(...)` call to use
   `functools.partial(async_fn, ...)`, which `iscoroutinefunction`
   *does* recognize.

**What's blocking the green run:** Orbstack/Docker has been flaky on
this machine — went down twice mid-test, taking the Postgres + Restate
containers with it. The Python code is ready; rerunning needs
`just up && just api && just chaos` against a stable Docker.

## Next session

1. `just up && just api`. Confirm `curl :8000/healthz` returns 200 and
   the registration response lists both `memory.echo` and
   `add_memory.run`.
2. `just chaos`. Expected green output: `extract_facts +
   decide_actions calls: 2 OK`. If it's 3, the partial→async fix
   didn't stick and extract was re-executed instead of replayed —
   check `inspect.iscoroutinefunction(partial(...))` on this Python
   version.
3. Update progress.md status table Phase 6 to `done`.
4. Stretch: write `just demo` that runs the golden path (POST → poll
   for SUCCEEDED → query memories) and then the chaos run, printing
   `DEMO OK` if both pass.
