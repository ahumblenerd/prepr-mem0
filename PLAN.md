# PLAN — Build order, TDD-driven, demoable + agent-verifiable per step

Each step lists:

- **Tests first** — the failing tests to write *before* any production code, in
  the order they should be written. This is the spine; everything else hangs
  off it.
- **Deliverable** — what gets added to the repo to turn those tests green.
- **Run** — exact command(s) to execute the step.
- **Verify** — deterministic assertion an agent can check (exit code, HTTP
  status, JSON shape). If `Verify` doesn't pass, the step is not done.

---

## TDD discipline (read once, applied everywhere)

### The rhythm

Per sub-step: **Red → Green → Refactor**, committed in that order. Each commit
either adds a failing test or makes one go green.

- **Red** — write the smallest possible test that asserts the next behavior. Run
  it. It must fail for the right reason (assertion, not import error).
- **Green** — write the minimum production code to flip it green. No bonus
  features.
- **Refactor** — clean up under the green light. Re-run the full unit suite —
  must stay green.

The agent verification at the end of each step is the green state of *all* the
tests written for that step, plus `just check`.

### Test taxonomy

| Layer            | Marker                          | What it can touch                              | Speed       |
| ---------------- | ------------------------------- | ---------------------------------------------- | ----------- |
| Unit             | none (default)                  | pure Python, in-memory mocks, fake clocks      | <50 ms each |
| Integration      | `@pytest.mark.integration`      | real Postgres (testcontainers), mocked LLM     | ~1 s each   |
| End-to-end       | `@pytest.mark.e2e`              | full docker compose, mocked LLM by default     | seconds     |
| Chaos            | `@pytest.mark.chaos`            | kills containers; only runs locally / nightly  | tens of s   |
| Live LLM smoke   | `@pytest.mark.live`             | hits real OpenRouter; gated by env, off in CI  | seconds     |

CI default: `pytest -m "not chaos and not live"` runs unit + integration + e2e.
Local default: same. Chaos and live are opt-in: `just chaos`, `just live`.

### Mocking boundaries (what is faked, what is real)

| Concern              | Unit tests                                | Integration tests                      | E2E / Chaos                           |
| -------------------- | ----------------------------------------- | -------------------------------------- | ------------------------------------- |
| LLM (OpenRouter)     | `respx` mocks the `httpx` transport       | same — `respx` with canned responses   | same by default; `live` mark hits real|
| Embeddings           | deterministic stub: `hash(text) → vec`    | same stub                              | same stub                             |
| Postgres + pgvector  | repo interface mocked at the seam         | **real** via `testcontainers-postgres` | **real** (the compose db)             |
| Restate Context      | fake `Context` that records `ctx.run`     | **real** Restate runtime via compose   | **real**                              |
| Time / `datetime.now`| `time-machine` freezes the clock          | real clock                             | real clock                            |
| UUIDs                | `monkeypatch` on `uuid.uuid4` for seq IDs | real                                   | real                                  |
| HTTP server          | `httpx.ASGITransport(app)` — no port      | same                                   | real uvicorn behind compose           |

The non-mockable layers are deliberate: pgvector's distance math, Restate's
journal replay, and OpenRouter's actual streaming behavior have killed projects
that thought they could fake them. They get real coverage at the integration /
chaos tier.

### Coverage gate

`pytest --cov=src/prepr_mem0 --cov-report=term-missing` runs as part of
`just check`. The `--cov-fail-under` floor ramps as we add code:

| After step | Floor |
| ---------- | ----- |
| 2          | 80%   |
| 3          | 85%   |
| 6          | 90%   |
| 11         | 92%   |

Coverage is a smell detector, not a goal — but a floor catches drift.

### What we deliberately don't unit-test

Wiring code (FastAPI routers' `include_router`, dependency injection plumbing,
the Restate service registration script) is exercised exclusively by integration
tests. Trying to unit-test wiring is the most common waste of TDD time in
FastAPI projects.

---

## Repo layout (incremental)

```
prepr/
├─ ARCH.md, PLAN.md, progress.md
├─ pyproject.toml
├─ justfile
├─ docker-compose.yaml
├─ migrations/
├─ scripts/
├─ src/prepr_mem0/
│   ├─ api/         # FastAPI app
│   ├─ workflow/    # restate service
│   ├─ db/          # sqlalchemy 2.x async + repos
│   ├─ llm/         # openrouter wrapper + prompts
│   └─ schemas/     # pydantic v2 models
├─ tests/
│   ├─ unit/
│   ├─ integration/
│   ├─ e2e/
│   ├─ chaos/
│   └─ conftest.py  # shared fixtures: pg container, fake restate ctx, respx
└─ sdk-python/      # generated, committed for drift check
```

`.env.example` ships with `OPENROUTER_API_KEY=`, `OPENROUTER_MODEL=`,
`DATABASE_URL=`, `RESTATE_INGRESS_URL=`.

---

## Step 0 — Repo skeleton + quality gate ✅

**Tests first**

- `tests/test_smoke.py::test_version_present` — asserts `__version__` is
  importable and truthy. The first red→green to prove the harness works.

**Deliverable:** `pyproject.toml` (ruff `ALL`, pyright strict, bandit, pytest),
`justfile`, `.pre-commit-config.yaml`, hello-world package.

**Run:** `uv sync && just check`.

**Verify:** exit 0. Plant `import os; x=1` → exit ≠ 0. Revert → exit 0.

Status: **done**. See `progress.md`.

---

## Step 1 — Postgres + pgvector in compose ✅

**Tests first**

- Phase 1 is pure infra; the "test" is the smoke command since there is no
  Python production code yet. Smoke covered by `just db-smoke` and the manual
  vector round-trip in `progress.md`. Real DB-integration tests land in Step 3.

**Deliverable:** `docker-compose.yaml` (`pgvector/pg16`, tmpfs PGDATA),
`migrations/0001_init.sql`, `scripts/migrate.sh`, `just up-db / migrate /
db-shell / db-sql / db-smoke`.

**Run / Verify:** see `progress.md` — green.

Status: **done**.

---

## Step 2 — FastAPI skeleton + auto OpenAPI

**Tests first** (all `tests/unit/api/test_app.py`)

1. `test_healthz_returns_ok` — GET `/healthz` → 200, body `{"ok": true}`. Red first.
2. `test_openapi_lists_v1_paths` — `/openapi.json` returns a doc whose `paths`
   includes all seven endpoints from ARCH §5 (`/v1/memories` GET+POST+DELETE,
   `/v1/memories/{id}`, `/v1/memories/{id}/history`, `/v1/memories/search`,
   `/v1/events/{event_id}`).
3. `test_openapi_includes_pydantic_schemas` — `components.schemas` contains
   `AddRequest`, `AddResult`, `MemoryItem`, `SearchRequest`, `SearchResult`,
   `EventStatus`.
4. `test_stub_endpoints_return_501` — POST `/v1/memories` etc. return 501
   "Not Implemented" until later steps wire real handlers.
5. `test_invalid_payload_returns_422` — POST `/v1/memories` with missing
   `user_id` → 422. Pydantic validation is contract.

All four use `httpx.AsyncClient(transport=ASGITransport(app=app))` — no
network, no port.

**Deliverable:** `src/prepr_mem0/api/app.py`, `schemas/` with pydantic v2
models, routes returning 501 with typed responses. `httpx` and `fastapi`
added as runtime deps; `respx`, `pytest-cov`, `time-machine` added as dev
deps. Coverage floor set to 80% in `pyproject.toml`.

**Run:**
```
just up-api &
curl -fsS localhost:8000/healthz
curl -fsS localhost:8000/openapi.json | jq '.paths | keys'
```

**Verify:** all unit tests green, `just check` exits 0 with coverage ≥ 80%.
Healthz returns `{"ok": true}`. The keys array contains every path from §5.
Visiting `/docs` renders.

---

## Step 3 — DB repository + sync `search` and `get` go live

**Tests first**

*Fixture work (one-time):* `tests/conftest.py` adds a session-scoped
`pg_container` fixture using `testcontainers-postgres`, runs `migrations/*.sql`
against it once, and yields an `AsyncEngine`. Per-test fixture truncates the
three tables.

1. `tests/integration/db/test_memory_repo.py::test_insert_then_get` — insert
   one memory, fetch by id, fields match including `embedding`.
2. `test_filter_by_user_id` — three rows for alice + two for bob; query alice
   returns three, bob returns two.
3. `test_filter_respects_soft_delete` — soft-delete one of alice's; filtered
   list now returns two.
4. `test_search_cosine_orders_by_distance` — insert three deterministic
   vectors v1, v2, v3 at known cosine distances from a probe; assert ordering.
5. `test_search_respects_threshold` — same setup; with `threshold=0.5`, v3
   (distant) is excluded.
6. `test_search_limit_caps_results` — insert 10 rows, `limit=3` returns 3.
7. `test_history_append_only` — write an ADD row; attempting `UPDATE memory_history`
   on it should be a code-level error (the repo has no update method).
8. `tests/unit/db/test_deterministic_embedder.py::test_same_text_same_vector`
   — the stub embedder is pure: same input → same 1536-d output.
9. `tests/unit/api/test_search_handler.py::test_search_handler_calls_repo`
   — handler-level unit with a `MagicMock` repo; asserts the handler hands
   off correct args (query string, filters, threshold, limit).
10. `tests/integration/api/test_search_e2e_app.py::test_search_returns_results`
   — via `ASGITransport` against the real repo + real DB, seed 3 rows, POST
   `/v1/memories/search` → returns ranked list.

**Deliverable:** SQLAlchemy 2.x async + asyncpg + Alembic (migrations move
from raw SQL to versioned), `db/models.py`, `db/repo.py`, deterministic
`embedder.stub.py`, real handlers for `GET /v1/memories`, `GET /v1/memories/{id}`,
`GET /v1/memories/{id}/history`, `POST /v1/memories/search`. `just seed`
script.

**Run:**
```
just up-db && just migrate && just seed && just up-api &
curl -fsS 'localhost:8000/v1/memories?user_id=alice' | jq 'length'
curl -fsS -XPOST localhost:8000/v1/memories/search \
  -H 'content-type: application/json' \
  -d '{"query":"hiking","user_id":"alice"}' | jq '.results | length'
pytest -m "not chaos and not live"
```

**Verify:** first returns `3`; second returns ≥ 1 with `score ∈ [0,1]`. All
integration tests green. Coverage ≥ 85%.

---

## Step 4 — Restate runtime + hello workflow

**Tests first**

1. `tests/unit/workflow/test_echo_handler.py::test_echo_returns_input` —
   build a fake `restate.Context`, invoke the handler function directly,
   assert return value. (The Restate Python SDK is testable as plain Python
   when the Context is dependency-injected.)
2. `tests/e2e/test_restate_invocation.py::test_send_invoke_echo` — real
   Restate + worker via compose; POST through Restate ingress, get response.
   Marked `@pytest.mark.e2e`.
3. `tests/e2e/test_restate_invocation.py::test_long_handler_resumes_after_kill`
   — invoke a 5-second sleep handler, `docker compose kill worker`, wait,
   `docker compose up -d worker`, poll until result returns. Asserts journal
   replay works. Marked `@pytest.mark.chaos`.

**Deliverable:** `restatedev/restate` added to compose, `src/prepr_mem0/workflow/echo.py`
service definition, `scripts/register_workflow.sh` and `just register` target,
`src/prepr_mem0/workflow/client.py` send-invoke helper for FastAPI.

**Run:**
```
just up && just register
curl -fsS -XPOST localhost:8080/memory/echo \
  -H 'content-type: application/json' -d '"ping"'
pytest -m "e2e or chaos"
```

**Verify:** echo returns `"ping"`; chaos test passes; Restate UI at
`localhost:9070` shows journals.

---

## Step 5 — OpenRouter wrapper + Mem0 prompts

**Tests first** (all `tests/unit/llm/`)

1. `test_openrouter_client.py::test_uses_openrouter_base_url` — instantiate
   client, assert `base_url == "https://openrouter.ai/api/v1"`.
2. `test_extract_facts.py::test_parses_clean_json_response` — `respx` returns
   `{"facts": ["fact1", "fact2"]}`; call extractor; assert list of two facts.
3. `test_extract_facts.py::test_strips_markdown_fences` — `respx` returns
   ` ```json\n{...}\n``` `; assert parser strips and returns facts.
4. `test_extract_facts.py::test_strips_think_tags` — response contains
   `<think>...</think>{"facts":[...]}`; assert parsed cleanly (matches mem0's
   `remove_code_blocks` behavior).
5. `test_extract_facts.py::test_normalizes_fact_dicts` — response is
   `{"facts": [{"fact": "x"}, "y"]}`; both forms accepted (matches
   `normalize_facts`).
6. `test_extract_facts.py::test_retries_on_429` — respx returns 429, then 200;
   assert eventual success + exactly two HTTP calls.
7. `test_extract_facts.py::test_gives_up_after_n_retries` — respx returns 429
   five times; assert raises after max retries.
8. `test_decide_actions.py::test_remaps_uuids_to_small_ints` — pass two memory
   UUIDs to the action determiner; assert the prompt the LLM saw contained
   ids `"0"` and `"1"`, not full UUIDs (intercepted via respx).
9. `test_decide_actions.py::test_remaps_response_back_to_uuids` — LLM
   returns `{"memory": [{"id":"0","event":"UPDATE","text":"x"}]}`; assert
   parsed action has the original UUID, not `"0"`.
10. `test_prompts.py::test_user_prompt_lifted_verbatim_from_mem0` — load
    `mem0/configs/prompts.py` upstream snapshot (committed under
    `tests/fixtures/upstream_prompts.txt`), assert exact match. Guards against
    silent drift.
11. `tests/integration/test_openrouter_live.py::test_extract_facts_live` —
    `@pytest.mark.live`. Real OpenRouter, gpt-4o-mini, message "I love hiking
    and drive a Tesla", assert ≥ 2 facts including substrings "hiking" /
    "Tesla". Skipped by default.

**Deliverable:** `src/prepr_mem0/llm/openrouter.py`, `llm/prompts.py` (lifted
from `mem0/configs/prompts.py`), `llm/sanitize.py` (`remove_code_blocks`,
`normalize_facts`, `extract_json`), `llm/extract.py`, `llm/decide.py`.
`openai` added as runtime dep; `respx` was added in Step 2.

**Run:**
```
pytest tests/unit/llm tests/integration/test_openrouter_mocked.py
OPENROUTER_API_KEY=$OPENROUTER_API_KEY pytest -m live
```

**Verify:** unit + integration green at `>=85%`. Live smoke (if key set)
prints fact list mentioning "hiking" and "Tesla".

---

## Step 6 — Durable `add_memory` workflow E2E

**Tests first**

*Unit tests, fake Context, all mocks:*

1. `tests/unit/workflow/test_add_orders_steps.py::test_step_order` — fake
   `Context` records `ctx.run` names. Run workflow with stubbed extractor /
   db / decider. Assert order: `create_event → extract_facts → search_neighbors
   → decide_actions → apply_actions → finish_event`.
2. `test_event_id_is_deterministic_per_invocation` — fake context returns
   fixed uuid from `ctx.uuid()`; assert returned `event_id` matches.
3. `test_workflow_returns_failed_status_on_extract_error` — extract stub
   raises; assert `finish_event` called with FAILED + error string.
4. `test_neighbors_run_in_parallel` — fake context records gather call;
   assert all per-fact neighbor lookups submitted before any awaited.

*Integration tests, real Postgres + Restate, mocked OpenRouter via respx:*

5. `tests/e2e/test_add_flow.py::test_post_returns_pending_then_succeeded` —
   POST `/v1/memories` returns `{event_id, status: PENDING}`; poll
   `/v1/events/{id}`; eventually `SUCCEEDED` with `result` containing
   `{memory_id, event=ADD, fact}` for each extracted fact.
6. `test_apply_actions_is_one_transaction` — inject a forced failure in the
   history insert; assert no memories row was committed either (atomicity).
7. `test_reconcile_no_duplicate_adds` — POST the same message twice; second
   `result` contains ≥1 `NONE` or `UPDATE`, no `ADD` for the same fact.
8. `test_uuid_remap_round_trip_on_update` — mock the decider's LLM to return
   an UPDATE keyed on the small-int id; assert the corresponding real UUID
   in the `memories` row gets the new content + an UPDATE row in
   `memory_history`.

**Deliverable:** `src/prepr_mem0/workflow/add_memory.py` (the workflow from
ARCH §6), `db/repo.py` gains `apply_actions_tx`, `apply_actions_tx`,
`create_event`, `finish_event`. `POST /v1/memories` wired to send-invoke.
`GET /v1/events/{id}` reads from `add_events`.

**Run:**
```
just up && just register
EV=$(curl -fsS -XPOST localhost:8000/v1/memories \
  -H 'content-type: application/json' \
  -d '{"user_id":"alice","messages":[{"role":"user","content":"I love hiking in the Cascades and I work at Mem0."}]}' \
  | jq -r .event_id)
until [ "$(curl -fsS localhost:8000/v1/events/$EV | jq -r .status)" = "SUCCEEDED" ]; do sleep 0.3; done
curl -fsS "localhost:8000/v1/events/$EV" | jq .result
pytest -m "not chaos and not live"
```

**Verify:** status reaches `SUCCEEDED`, ≥ 2 ADD entries. Re-post: actions
include `NONE`/`UPDATE`, no dup ADDs. Coverage ≥ 90%.

---

## Step 7 — Chaos test (the durability money shot)

**Tests first**

1. `tests/chaos/test_resume_after_crash.py::test_extract_then_kill_then_resume`
   — set `CHAOS=after_extract_facts` env on worker; POST add; sleep 1 s;
   `docker compose kill worker`; sleep 2 s; `docker compose up -d worker`;
   poll until SUCCEEDED; assert: (a) event reached SUCCEEDED, (b) exactly
   **one** request hit the `respx`-mocked OpenRouter `extract_facts` endpoint
   over the entire run, (c) Restate UI shows the step as "Completed (from
   journal)" after restart.
2. `test_kill_during_apply_actions` — `CHAOS=mid_apply_actions` raises before
   committing the tx; restart; assert no half-written history rows; single
   SUCCEEDED event; final `memories` count matches expected.
3. `test_kill_during_decide_actions` — same shape, mid-LLM-call-2.

**Deliverable:** `src/prepr_mem0/workflow/chaos.py` reads `CHAOS` env and
raises `SystemExit(1)` at the named hook. `scripts/chaos.sh` orchestrates
the kill/restart. `just chaos` runs the test class.

**Run:**
```
just chaos
```

**Verify:** test class green; the `respx` call counter assertion is what
proves durable execution rather than naive retry.

This is the project's headline behavior.

---

## Step 8 — Generated SDK + drift check

**Tests first**

1. `tests/integration/sdk/test_generated_sdk.py::test_add_poll_search_via_sdk`
   — import the freshly generated client, run add → poll → search, all
   against the live FastAPI app via `ASGITransport`. Mocked OpenRouter.
2. `test_sdk_drift_clean.py::test_no_uncommitted_sdk_changes` — runs
   `openapi-python-client generate ...` into a temp dir; `diff -r`
   against committed `sdk-python/`; assert empty.

**Deliverable:** `openapi-python-client` in dev deps. `just gen-sdk` target.
`sdk-python/` committed. Smoke script `sdk-python/smoke.py` for manual
demos.

**Run:**
```
just gen-sdk
pytest tests/integration/sdk
```

**Verify:** both tests green. Drift test fails if API or generator output
changes without regen.

---

## Step 9 — Full lint gate in CI

**Tests first**

1. `tests/meta/test_check_passes_on_main.py` — runs `subprocess.run(["just",
   "check"])`, asserts exit 0. This is the meta-test that protects the
   gate itself from accidental disablement (e.g., someone adds `--no-strict`
   to pyright in pyproject).
2. CI workflow `.github/workflows/ci.yaml` matches `just check` step-for-step.

**Deliverable:** `.github/workflows/ci.yaml`, pre-commit installed on the
repo. `just check` confirmed green on a fresh clone.

**Run:**
```
just check
gh workflow run ci   # if pushing to a fork
```

**Verify:** green on `main`; planted violations (`# type: ignore` removed,
`os.system` for bandit, renamed endpoint for SDK drift) each fail
independently.

---

## Step 10 — Observability

**Tests first**

1. `tests/unit/obs/test_structlog_emits_event_id.py` — within a workflow
   step, structlog adds `event_id` to every log line via contextvars; capture
   via `caplog`, assert presence.
2. `tests/unit/obs/test_otel_span_per_ctx_run.py` — fake OTel exporter; run
   workflow; assert one span per named `ctx.run`.
3. Manual: `just trace` prints a span tree for the most recent event.
4. Manual: Restate UI at `localhost:9070` shows the invocation.

**Deliverable:** `structlog` configured, OTel SDK + console exporter, span
wrappers around `ctx.run`, `just trace`.

**Run / Verify:** unit tests green; trace tree shows `add_memory >
extract_facts > openrouter.chat`; UI lists invocations.

---

## Step 11 — One-shot demo

**Tests first**

1. `tests/e2e/test_demo_script.py::test_demo_returns_zero` — runs `just
   demo` as a subprocess; asserts exit 0 and stdout ends with `DEMO OK`.
   This is the "the entire system works" assertion.

**Deliverable:** `just demo` orchestrates: clean stack → up → register →
migrate → seed → golden POST/poll/search → reconcile POST → chaos test →
SDK smoke → "DEMO OK" footer.

**Run:** `just demo`.

**Verify:** subprocess returns 0; wall time < ~90 s warm OpenRouter.
Coverage ≥ 92%.

---

## Stretch

- TypeScript SDK via `@hey-api/openapi-ts` + a `node sdk-ts/smoke.mjs`. Same
  add → poll → search shape.
- Hybrid search — BM25 via Postgres `tsvector` + `score_and_rank` mirroring
  `mem0/utils/scoring.py`. Adds a test case to `test_search_*`.
- Webhooks — `POST /v1/webhooks/{id}` + outbound POST from `finish_event`.
  Tested via `respx` capturing the outbound call.
- Graph layer stub — second Restate handler `add_memory_graph` running in
  parallel to vector path. Talks to the Neptune/Neo4j seam without committing
  to building it.

---

## What this project demonstrates

1. Deep modeling of Mem0's `add` pipeline — two LLM calls, UUID anti-hallucination
   trick, reconcile semantics, SQLite-history schema, V3 `async_mode` event
   contract — reproduced on a different runtime.
2. Durable execution where it earns its keep: the partial-write + retry surface
   between two LLM calls and a multi-row mutation.
3. Tests-first: every behavior has a test that came before the code; the chaos
   test makes the durability claim verifiable, not rhetorical.
4. Reproducible: one `just up`, one `just demo`. Strict lint gate, coverage
   floor, all under a single task runner.
