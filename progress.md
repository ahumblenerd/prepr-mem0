# Progress

Live tracker for the build laid out in [PLAN.md](./PLAN.md). Each phase has a
**Verify** column an agent (or interviewer) can re-run from a clean checkout.

Last updated: 2026-05-18.

| Phase | Status | One-line summary |
| ----- | ------ | ---------------- |
| 0 — Repo skeleton + quality gate | ✅ done | `just check` enforces ruff (ALL) + pyright strict + bandit + pytest |
| 1 — Postgres + pgvector in compose | ✅ done | `just up-db && just migrate && just db-smoke` brings up `pgvector/pg16` on tmpfs with the 3-table schema |
| 2 — FastAPI skeleton + auto OpenAPI | ⏭ next | stubs for the full Mem0 v1 surface, `/openapi.json` consumable |
| 3 — DB repo + sync `search` and `get` | ⏳ pending | sqlalchemy 2.x async, alembic, deterministic-embedding stub |
| 4 — Restate runtime + hello workflow | ⏳ pending | restate container in compose, `just register`, echo handler |
| 5 — OpenRouter wrapper + prompts | ⏳ pending | lifted Mem0 prompts; mocked + live smoke |
| 6 — Durable `add_memory` E2E | ⏳ pending | `POST /v1/memories` returns event_id, workflow runs to `SUCCEEDED` |
| 7 — Chaos test | ⏳ pending | crash worker mid-flight; prove no double LLM call from journal |
| 8 — Generated SDK + drift check | ⏳ pending | `openapi-python-client`, CI guard on diff |
| 9 — Full lint gate in CI | ⏳ pending | `.github/workflows/ci.yaml` mirrors `just check` |
| 10 — Observability | ⏳ pending | structlog + OTel spans; Restate UI exposed |
| 11 — One-shot demo | ⏳ pending | `just demo` runs golden path + chaos + SDK smoke |

---

## Phase 0 — Repo skeleton + quality gate ✅

**Files landed**

```
pyproject.toml              # ruff (select=ALL), pyright strict, bandit, pytest
justfile                    # sync / fmt / check / lint / typecheck / security / test / hooks
.pre-commit-config.yaml     # ruff + pyright + bandit + hygiene hooks
.python-version             # 3.12
.gitignore
src/prepr_mem0/__init__.py
tests/test_smoke.py
```

**Decisions**

- `uv` over `hatch` for package management — single fast resolver, no env activation gymnastics.
- Ruff `select = ["ALL"]` with a curated ignore list (`D`, `COM812`, `ISC001`, `FIX`, `TD`, `CPY`, `FBT`, `PLR0913`). Maximally strict by default; turn off rules with intent.
- Pyright strict mode for both `src/` and `tests/` — typing the tests is the cheapest way to make refactors safe.
- Bandit excludes `tests/` only.
- `just` over `make` — tab-character traps and shell quoting in Makefiles are the same source of pain we're trying to avoid in our actual workflow code.

**Verified**

| Check | Command | Expected | Got |
| ----- | ------- | -------- | --- |
| Sync resolves | `uv sync` | exit 0, Python 3.12.12 venv | ✅ |
| Gate green | `just check` | exit 0 (ruff format, ruff lint, pyright, bandit, pytest) | ✅ exit 0 |
| Gate fires on a plant | append `import os\nx=1` to `__init__.py`, `just check` | exit ≠ 0, fails on ruff format first | ✅ exit 1 |
| After revert | `just check` | exit 0 again | ✅ exit 0 |

**Notes for next session**

- `just` was installed via Homebrew during Phase 0. Reversible with `brew uninstall just`.
- Repo isn't a git init yet. Recommend `git init && git add -A && git commit -m "chore: phase 0+1"` before Phase 2 to get an undo button.

---

## Phase 1 — Postgres + pgvector in compose ✅

**Files landed**

```
docker-compose.yaml         # pgvector/pgvector:pg16, tmpfs-backed PGDATA, port 5433
migrations/0001_init.sql    # memories / memory_history / add_events + indexes
scripts/migrate.sh          # lexical-order migration runner; replaced by alembic in Step 3
justfile                    # +up-db, +down-db, +migrate, +db-shell, +db-sql, +db-smoke
```

**Decisions**

- **Single Postgres for vectors + history + events** — mirrors ARCH.md §4. Collapsing Mem0's Qdrant+SQLite split into one source of truth removes the partial-write surface our durable workflow is meant to handle. The interview talking point is *why* a real deployment would split them again at scale (different IO profiles, vector index hot-path shouldn't share locks with OLTP), not that this demo collapses them.
- **tmpfs PGDATA** — boot is ~1 s, container restart wipes data. Exactly the "in-memory" semantics asked for. Flip one compose line to switch to a named volume if needed.
- **Port 5433 on the host** — keeps any existing local Postgres on 5432 untouched.
- **pgcrypto** for `gen_random_uuid()` so application code never has to generate UUIDs for the DB to accept — keeps inserts simple.
- **`ivfflat` with `lists=100`** — fine up to ~1M rows. Emits a "low recall" notice on an empty table; harmless. Will tune in Step 3.
- **Soft delete** via `deleted_at` + partial indexes — `WHERE deleted_at IS NULL`. Lets history reads stay correct after a `DELETE` event.
- **CHECK constraints** on `event` and `status` columns — push schema invariants into the DB instead of trusting application code.
- **Raw `.sql` migrations** for now — moving to Alembic in Step 3 once we have SQLAlchemy models. Avoids dragging in Alembic for one file.

**Verified**

| Check | Command | Expected | Got |
| ----- | ------- | -------- | --- |
| Container up + healthy | `just up-db` | `pg_isready` returns | ✅ |
| Schema applied | `just migrate` | "migrations done" | ✅ |
| Extensions present | `just db-sql "SELECT extname FROM pg_extension WHERE extname IN ('vector','pgcrypto') ORDER BY extname;"` | `pgcrypto`, `vector` | ✅ |
| Tables present | `just db-sql "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;"` | `add_events`, `memories`, `memory_history` | ✅ |
| 1536-dim vector round-trip | insert with `array_fill(0.1, ARRAY[1536])::vector`, cosine distance to self | distance `0` | ✅ |
| Quality gate still green | `just check` | exit 0 | ✅ |

**Notes**

- `tmpfs` means restart = data loss. If you `docker compose restart db`, the next thing you must do is `just migrate`. The full demo flow will encode this in `just up`.
- Hit one snag: `just`'s `*ARGS` passthrough mangles quoted SQL when paired with `set shell := ["bash", "-cu"]`. Split into two recipes — `db-shell` (interactive) and `db-sql SQL` (one-shot, uses `{{quote(SQL)}}`).

---

## Discipline change — TDD goes in writing

PLAN.md was rewritten to make **intense TDD** the spine, not a footnote.

Highlights:

- **Red → Green → Refactor** per sub-step, committed in that order. Each commit
  either adds a failing test or makes one green.
- **Test taxonomy** with explicit markers: `integration`, `e2e`, `chaos`,
  `live`. CI runs `not chaos and not live` by default.
- **Mocking boundaries** spelled out:
  - LLM (OpenRouter): `respx` mocks at the `httpx` transport everywhere; one
    optional `@pytest.mark.live` smoke per LLM function.
  - Embeddings: deterministic stub function for all tests.
  - Postgres + pgvector: **never mocked** — real container via
    `testcontainers-postgres` for integration, the compose db for e2e.
  - Restate Context: fake `Context` records `ctx.run` calls for unit tests;
    real runtime for integration / e2e / chaos.
  - Time / UUIDs: `time-machine` + `monkeypatch` for determinism.
- **Coverage floor** in `just check`: ramps 80% (after Step 2) → 85% → 90% →
  92%.
- **Per-step red-test lists** — every step now opens with the exact failing
  tests to write before any production code lands.

Mem0 cares about quality and the senior signal here is "I work tests-first and
treat the mock boundary as architecture." This change makes that legible in the
plan itself.

## Next up — Phase 2

Stand up FastAPI with the full Mem0 v1 endpoint surface as 501 stubs. **Tests
first** per PLAN.md Step 2:

1. `test_healthz_returns_ok`
2. `test_openapi_lists_v1_paths`
3. `test_openapi_includes_pydantic_schemas`
4. `test_stub_endpoints_return_501`
5. `test_invalid_payload_returns_422`

Dev deps to add this phase: `fastapi`, `httpx`, `respx`, `pytest-cov`,
`time-machine`. Coverage floor flips on at 80%.
