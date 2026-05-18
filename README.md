# prepr-mem0

A demo of a durable, Mem0-style memory API built on **Restate** + **FastAPI** +
**Postgres/pgvector** + **OpenRouter**.

The motivating idea: Mem0's `Memory.add()` pipeline is two LLM calls reconciling
against a vector store and an append-only history. That's exactly the workload
durable execution exists for — so this project puts a Restate workflow in front
of it. A crash mid-flight resumes from the journal instead of double-charging
the LLM.

## Stack

| Layer        | Choice                                                  |
| ------------ | ------------------------------------------------------- |
| HTTP edge    | FastAPI (Python 3.12), auto-emitted OpenAPI             |
| Durable core | Restate runtime + `restate-sdk` (Python)                |
| LLM          | OpenRouter via `openai` SDK with `base_url` override    |
| Datastore    | Postgres 16 + pgvector, single ephemeral tmpfs container|
| Lint / types | ruff (`select = ALL`), pyright strict, bandit           |
| Task runner  | `just`                                                  |

## Quickstart

Requirements: `docker`, `uv`, `just` (`brew install just`).

```bash
uv sync
just up           # postgres + restate + migrations + worker + register
just api          # FastAPI on :8000
just check        # ruff + pyright + bandit + pytest --cov (80% floor)
```

Smoke the Restate path:

```bash
curl -s -X POST http://localhost:8080/memory/echo \
    -H 'content-type: application/json' -d '"ping"'
# → "ping"
```

## Layout

```
src/prepr_mem0/
├─ api/         # FastAPI app — edge layer
├─ db/          # SQLAlchemy 2.x async models + repo
├─ embeddings.py# deterministic embedding stub (swap for real provider)
├─ schemas/     # pydantic v2 request/response models
└─ workflow/    # restate services (echo + add_memory)
migrations/     # raw SQL, idempotent
tests/
├─ integration/ # ASGITransport + live postgres
└─ ...
```

## Status

| Phase | What                                                  | State |
| ----- | ----------------------------------------------------- | ----- |
| 0     | Repo skeleton, ruff/pyright/bandit/pytest gate         | done  |
| 1     | Postgres + pgvector schema (memories / history / events) | done  |
| 2     | DB repo, FastAPI skeleton, deterministic embedder      | done  |
| 3     | Restate runtime + echo workflow, end-to-end invocation | done  |
| 4     | OpenRouter wrapper + fact-extraction / action prompts  | wip   |
| 5     | Durable `add_memory` workflow (`ctx.run` per side effect) | wip |
| 6     | Chaos demo: kill worker mid-flight, journal-replay     | wip   |

## Design docs

- [`ARCH.md`](ARCH.md) — architecture, data model, workflow shape
- [`PLAN.md`](PLAN.md) — phased build order with per-step verification
- [`progress.md`](progress.md) — running log
