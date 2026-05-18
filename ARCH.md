# ARCH — Durable Mem0-style API on Restate + FastAPI

> Project goal: replicate the most interesting flow in Mem0's open-source memory
> system — `Memory.add()` — on a durable workflow engine, behind a typed REST API,
> in a single `docker compose up`. Built as a study of where durable execution
> earns its keep when an API does multiple LLM calls plus reconciling writes.

## 1. Why this shape

Mem0's `Memory.add()` is the single best workflow to demo durability on. From the docs
and source:

1. **Fact extraction** — LLM call against `USER_MEMORY_EXTRACTION_PROMPT` or
   `AGENT_MEMORY_EXTRACTION_PROMPT` returning a list of facts.
2. **Neighbor retrieval** — vector search for existing memories per fact.
3. **Action determination** — second LLM call (`get_update_memory_messages`) emitting
   `ADD | UPDATE | DELETE | NONE` per fact, with UUIDs remapped to small ints to
   prevent hallucination.
4. **Apply** — write vectors + `history(event=ADD|UPDATE|DELETE)` rows. Partial-write
   risk across vector + history.
5. **Return** — Platform V3 returns an `event_id` immediately (`async_mode=True`,
   `PENDING → RUNNING → SUCCEEDED | FAILED`).

Two network LLM calls, a multi-row mutation, and an externalized async-event contract.
Exactly the workload durable execution exists for.

## 2. Stack

| Layer        | Tech                                                  | Why                                                                                                |
| ------------ | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| HTTP edge    | **FastAPI** (Python 3.12)                             | Pydantic-v2 first-class, native OpenAPI emission, async by default                                 |
| Durable core | **Restate** runtime + **restate-sdk-python**          | Journaled `ctx.run()` makes LLM calls + DB writes replay-safe; built-in event ID + status          |
| LLM          | **OpenRouter** via `openai` Python SDK (custom base)  | One key, many models; lets us swap `gpt-4o-mini` ↔ `claude-haiku` ↔ `llama-3.1-70b` for the demo  |
| Datastore    | **Postgres 16 + pgvector** (single ephemeral Docker)  | Replaces both Mem0's vector store and `SQLiteManager` history with one truth source                |
| SDK gen      | **`openapi-python-client`** (+ `@hey-api/openapi-ts`) | Generates a typed, async, Pydantic-v2 client straight from FastAPI's `/openapi.json`               |
| Lint/format  | **ruff** + **pyright** (strict) + **bandit**          | Single fast Rust-based formatter+linter, strict typing, security baseline                          |
| Orchestration| **`just`** + **docker compose**                       | `just up`, `just demo`, `just check`. Every step an agent can run                                  |

> "Postgres in memory" interpreted as a single ephemeral Postgres container
> (`tmpfs`-backed `PGDATA` for instant boot, no host volume). If a real on-disk volume
> is preferred, flip one compose line.

## 3. Component diagram

This is the shape that's actually running on disk and verified end-to-end
against real Anthropic Claude Haiku 4.5 via OpenRouter:

```
┌─────────────┐      POST /v1/memories                  ┌─────────────────────┐
│   Caller    │ ──────────────────────────────────────► │   FastAPI (:8000)   │
│  curl / SDK │                                          │   prepr_mem0.api    │
│             │ ◄── 202 { event_id, "PENDING" } ──────  │   /healthz /docs    │
└─────────────┘                                          └──────────┬──────────┘
                                                                    │
                                                                    │  generic_send(
                                                                    │    service="add_memory",
                                                                    │    key=event_id,
                                                                    │    arg=AddRequest JSON,
                                                                    │    content-type=application/json)
                                                                    ▼
                            ┌─────────────────────────────────────────────────────────────┐
                            │              Restate runtime (:8080 ingress, :9070 admin)   │
                            │ ─────────────────────────────────────────────────────────── │
                            │  • Journals each ctx.run(...) step + its serialized result  │
                            │  • Retries on transient failure                             │
                            │  • Replays journal on worker crash (= no double LLM calls)  │
                            └─────────────────────────────┬───────────────────────────────┘
                                                          │
                                              HTTP/2      │  POST /invoke/add_memory/run
                                                          ▼
                                ┌────────────────────────────────────────────────────────┐
                                │   Worker (:9080) — uvicorn(prepr_mem0.workflow.asgi)    │
                                │ ────────────────────────────────────────────────────── │
                                │   add_memory_wf @ Workflow keyed by event_id           │
                                │                                                        │
                                │   async def run_add_memory(ctx, req):                  │
                                │     event_id = UUID(ctx.key())                         │
                                │     ↓                                                  │
                                │  [1] ctx.run("create_event",  …)          ──► Postgres │
                                │     ↓                                                  │
                                │  [2] ctx.run("extract_facts", …)          ──► OpenRouter (LLM call #1)
                                │     ↓                          maybe_crash("after_extract_facts")
                                │  [3] for i,fact in enumerate(facts):                   │
                                │       ctx.run(f"knn:{i}", …)            ──► Postgres + pgvector
                                │     ↓                                                  │
                                │  [4] ctx.run("decide_actions", …)         ──► OpenRouter (LLM call #2)
                                │     ↓                            (UUIDs remapped to small ints
                                │     ↓                             so Haiku doesn't hallucinate them)
                                │  [5] ctx.run("apply_actions", …)          ──► Postgres tx
                                │       (writes memories + memory_history atomically)    │
                                │     ↓                                                  │
                                │  [6] ctx.run("finish_event", …)           ──► Postgres │
                                │     ↓                                                  │
                                │   return AddResult(event_id, "SUCCEEDED")              │
                                └───────────────┬──────────────────────┬─────────────────┘
                                                │                      │
                              ┌─────────────────▼────────┐   ┌─────────▼─────────────────┐
                              │   OpenRouter             │   │   Postgres 16 + pgvector  │
                              │   openai SDK +           │   │   (Docker, tmpfs PGDATA)  │
                              │   base_url override      │   │                           │
                              │                          │   │   ┌─────────────────────┐ │
                              │   anthropic/             │   │   │ memories            │ │
                              │   claude-haiku-4.5       │   │   │  id, user_id,       │ │
                              │                          │   │   │  content, embedding │ │
                              │   2 calls/workflow:      │   │   │  (vector(1536))     │ │
                              │   • USER_MEMORY_EXTRACT  │   │   └─────────────────────┘ │
                              │   • update_memory_       │   │   ┌─────────────────────┐ │
                              │     template (decide)    │   │   │ memory_history      │ │
                              │                          │   │   │  ADD/UPDATE/DELETE  │ │
                              │   respx-mocked in        │   │   └─────────────────────┘ │
                              │   tests; fake_openrouter │   │   ┌─────────────────────┐ │
                              │   server in chaos run    │   │   │ add_events          │ │
                              │                          │   │   │  PENDING|RUNNING|   │ │
                              │                          │   │   │  SUCCEEDED|FAILED   │ │
                              │                          │   │   │  + result jsonb     │ │
                              │                          │   │   └─────────────────────┘ │
                              └──────────────────────────┘   └───────────────────────────┘

                              GET /v1/events/{event_id}   ──► reads add_events directly
                                                              (no Restate involved)
```

**Read this as:** FastAPI is a thin edge that does nothing except generate
an event_id and `send_invoke` the durable workflow. The workflow body is a
plain async Python function — six `ctx.run(...)` calls in a row. Restate's
job is to journal each step's return value, so when the worker dies after
`extract_facts` returns, the restarted worker replays from the journal and
the cached `["Name is Arun", ...]` list is returned instead of re-calling
OpenRouter. That is the entire durability story in one sentence.

**What Restate isn't doing:** retries-of-our-own, idempotency keys,
dedup table, distributed locks. It's all journal-and-replay. The DB
transaction inside `apply_actions` is the only homegrown atomicity
we keep, because writing memories + memory_history is one logical
write and we don't want a partial state if `_apply_actions_tx`
crashes mid-loop.

**Verified end-to-end on 2026-05-18** against Anthropic Claude Haiku
4.5 via OpenRouter: POST → SUCCEEDED in ~4s, three facts extracted
from `"My name is Arun, I drink earl grey tea every morning, and my
favorite city is Lisbon"` landed in `memories`.

## 4. Data model (Postgres)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE memories (
  id              uuid PRIMARY KEY,
  user_id         text NOT NULL,
  agent_id        text,
  run_id          text,
  content         text NOT NULL,
  content_hash    text NOT NULL,                       -- md5(content), skip redundant updates
  embedding       vector(1536) NOT NULL,
  metadata        jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  deleted_at      timestamptz
);
CREATE INDEX memories_user_idx       ON memories (user_id) WHERE deleted_at IS NULL;
CREATE INDEX memories_embedding_idx  ON memories USING ivfflat (embedding vector_cosine_ops);

CREATE TABLE memory_history (              -- mirrors Mem0 SQLiteManager.history
  id            uuid PRIMARY KEY,
  memory_id     uuid NOT NULL,
  old_memory    text,
  new_memory    text,
  event         text NOT NULL CHECK (event IN ('ADD','UPDATE','DELETE')),
  actor_id      text,
  role          text,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE add_events (                  -- mirrors Platform V3 async_mode event
  id            uuid PRIMARY KEY,          -- = event_id returned to caller
  user_id       text NOT NULL,
  status        text NOT NULL CHECK (status IN ('PENDING','RUNNING','SUCCEEDED','FAILED')),
  latency_ms    integer,
  error         text,
  result        jsonb,                     -- list of {memory_id, event, fact}
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);
```

This deliberately collapses Mem0's split (Qdrant + SQLite) into one Postgres so the
demo has one moving part less. At real scale you'd split them again — different
IO profiles, vector index hot-path doesn't want OLTP locks — but for this
project, one container, one truth source.

## 5. Public API surface

Modeled on Mem0's v1, with Platform V3's `async_mode` semantics baked in.

| Method & path                         | Behavior                                                                                   |
| ------------------------------------- | ------------------------------------------------------------------------------------------ |
| `POST   /v1/memories`                 | Enqueue `add_memory` workflow. Returns `{event_id, status: "PENDING"}`.                    |
| `GET    /v1/events/{event_id}`        | Poll workflow status; returns `result` once `SUCCEEDED`.                                   |
| `POST   /v1/memories/search`          | Synchronous vector search (no LLM, no Restate needed).                                     |
| `GET    /v1/memories`                 | List by `user_id` / `agent_id` / `run_id` filters.                                         |
| `GET    /v1/memories/{id}`            | Single memory.                                                                             |
| `GET    /v1/memories/{id}/history`    | Audit trail.                                                                               |
| `DELETE /v1/memories/{id}`            | Soft delete; logs `DELETE` to `memory_history`.                                            |
| `GET    /openapi.json`, `/docs`       | Auto-emitted; the SDK is generated from this.                                              |

Why split `add` (async, durable) from `search` (sync): mirrors Mem0's choice — `add`
has two LLM calls and is naturally an async event; `search` is one embed + one
`SELECT ... ORDER BY embedding <=> $1` and shouldn't pay the workflow tax.

## 6. The durable `add_memory` workflow

```python
# services/workflow.py (sketch)
import restate

mem_svc = restate.Service("memory")

@mem_svc.handler(name="add")
async def add(ctx: restate.Context, req: AddRequest) -> AddResult:
    event_id = ctx.uuid()                                          # deterministic
    await ctx.run("create_event_row", lambda: db.create_event(event_id, req.user_id))

    facts = await ctx.run("extract_facts",
                          lambda: openrouter.extract_facts(req.messages, req.agent_id))

    # parallel side effects, each individually journaled
    neighbors = await ctx.gather([
        ctx.run(f"neighbors:{i}", lambda f=f: db.knn(f, req.user_id, k=5))
        for i, f in enumerate(facts)
    ])

    actions = await ctx.run("decide_actions",
                            lambda: openrouter.decide_actions(facts, neighbors))

    result = await ctx.run("apply_actions",
                           lambda: db.apply_actions_tx(actions, req.user_id))   # one tx

    await ctx.run("finish_event", lambda: db.finish_event(event_id, result))
    return AddResult(event_id=event_id, result=result)
```

**What durability buys us, concretely:**

- Crash between `extract_facts` and `decide_actions`: Restate replays from journal,
  `extract_facts` returns its cached result, no second OpenRouter charge.
- OpenRouter 429 / 5xx: configured retry policy on the `ctx.run` step, not in our
  code.
- Postgres connection dropped mid-`apply_actions`: the tx aborts cleanly; Restate
  retries the whole `apply_actions` step idempotently (we keyed it by `event_id` +
  fact index so reapplication is a no-op).
- Caller crash: irrelevant — workflow continues; caller polls `/v1/events/{id}`.

## 7. OpenRouter integration

Use the `openai` Python SDK with `base_url="https://openrouter.ai/api/v1"` and
`OPENROUTER_API_KEY`. Two prompts, lifted from `mem0/configs/prompts.py`:

- `USER_MEMORY_EXTRACTION_PROMPT` — returns `{"facts": ["..."]}`.
- `update_memory_template` — returns `{"memory": [{"id": "0", "event": "ADD",
  "text": "..."}, ...]}` with UUIDs remapped to small ints.

Both calls go through `instructor` or a hand-rolled JSON-schema response so we get
typed outputs without parser yak-shaving. Embedding via OpenRouter's embedding
endpoint (or fall back to `text-embedding-3-small` direct if OpenRouter doesn't
proxy that model).

## 8. Generated SDK

`openapi-python-client generate --path openapi.json --output-path sdk-python`
emits an `httpx`-based async client with Pydantic v2 models. The demo includes a
~20-line script that imports the generated SDK and runs `add → poll → search`,
proving the contract is real:

```python
from prepr_mem0_client import Client
from prepr_mem0_client.api.memories import add_memories, poll_event, search_memories

async with Client(base_url="http://localhost:8000") as c:
    ev = await add_memories.asyncio(client=c, body=AddRequest(...))
    while (e := await poll_event.asyncio(client=c, event_id=ev.event_id)).status != "SUCCEEDED":
        await asyncio.sleep(0.2)
    print(await search_memories.asyncio(client=c, body=SearchRequest(query="...")))
```

TypeScript SDK as a stretch: `@hey-api/openapi-ts` against the same spec. Same
demo, JS flavor.

## 9. Quality bar

`pyproject.toml`:

- `[tool.ruff]` — `select = ["ALL"]` with a short ignore list (`D`, `ANN101`,
  `COM812`). `line-length = 100`. `target-version = "py312"`.
- `[tool.pyright]` — `strict = true`, `reportMissingTypeStubs = "warning"`.
- `[tool.bandit]` — default profile.
- `[tool.pytest.ini_options]` — `asyncio_mode = "auto"`, `addopts = "-x --strict-markers"`.
- `pre-commit` runs ruff, pyright, bandit, prettier (for the gen'd TS) on every
  commit. CI mirrors the same `just check` target.

Test layers:

- **Unit** — pure functions: prompt builders, UUID remapper, action applier.
- **Integration** — real Postgres via `testcontainers`; real Restate via the
  compose stack; OpenRouter mocked at the `httpx` transport layer with `respx`.
- **E2E** — `just demo` script that runs the full path and asserts on exit
  codes and JSON shapes.

## 10. Non-goals

- Graph memory — Mem0's Neptune/Neo4j layer is a separate workflow; same shape.
- Multi-tenant auth — single `X-Api-Key` header gate, no orgs/projects.
- Reranking / hybrid BM25 — pgvector cosine only; mention as a one-line extension.
- Production deployment — Restate has a hosted offering, but the demo is
  self-contained docker-compose.

## 11. The thirty-second summary

Mem0's `add` is two LLM calls and a reconciling write across a vector store and
a history table. That's exactly the workload durable execution was built for,
so this project puts Restate in front of it: the FastAPI edge enqueues an
`add` workflow and hands back an event ID — the same shape as Mem0's Platform
V3 `async_mode`. Each LLM call and each DB write is a journaled side effect,
so a mid-workflow crash doesn't charge OpenRouter twice or leave half-written
history. One `just up` brings the whole thing up; one `just demo` runs the
golden path plus a forced-crash test that shows the workflow resuming from
its journal.
