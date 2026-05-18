# ARCH — Durable Mem0-style API on Restate + FastAPI

> Demo target: replicate Mem0's most interesting flow — `Memory.add()` — on a durable
> workflow engine, behind a typed REST API, with an auto-generated SDK, in a single
> `docker compose up`. Audience: Mem0 senior backend interview.

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

```
+---------------------+     POST /v1/memories        +-----------------------+
|   Caller / Test     | ---------------------------> |   FastAPI (edge)      |
|   (curl, gen SDK)   |  <-- {event_id, PENDING} --- |  /openapi.json,/docs  |
+---------------------+                              +-----------+-----------+
                                                                 |
                                                  send-invoke    |  HTTP/2 ingress
                                                                 v
                          +-------------------------- Restate Runtime ------------------------+
                          |   journals + retries + replay + state + scheduler                 |
                          |                                                                   |
                          |   workflow add_memory(req)  :: durable service                    |
                          |     1. ctx.run("extract_facts")  -> OpenRouter (Side Effect)      |
                          |     2. ctx.run("search_neighbors", per-fact, parallel) -> pgvec   |
                          |     3. ctx.run("decide_actions") -> OpenRouter (Side Effect)      |
                          |     4. ctx.run("apply_actions")  -> Postgres tx (mem + history)   |
                          |     5. set event status = SUCCEEDED                               |
                          +-------------------+---------------------+-------------------------+
                                              |                     |
                              +---------------v------+    +---------v-----------+
                              |  OpenRouter (LLM)    |    | Postgres + pgvector |
                              |  models: openrouter/*|    |  memories, history, |
                              |                      |    |  events             |
                              +----------------------+    +---------------------+
```

Restate is a sidecar **runtime**. Our Python "workflow service" is a normal HTTP
service Restate calls into; it replies with journal entries Restate persists. On
crash/restart, Restate re-invokes us and feeds back the journal so any side effect
that already returned is **not re-executed**. That is what makes the LLM calls and
DB writes safe under retry without homegrown idempotency keys.

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
demo has one moving part less. The interview talking point is *why* you'd split them
at scale (different IO profiles, vector index hot-path doesn't want OLTP locks) —
not *that* this demo splits them.

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
proxy that model on demo day).

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
- **E2E** — `just demo` script the agent (or the interviewer) runs, asserts on
  exit codes and JSON shapes.

## 10. Non-goals (call out in interview)

- Graph memory — Mem0's Neptune/Neo4j layer is a separate workflow; same shape.
- Multi-tenant auth — single `X-Api-Key` header gate, no orgs/projects.
- Reranking / hybrid BM25 — pgvector cosine only; mention as a one-line extension.
- Production deployment — Restate has a hosted offering, but the demo is
  self-contained docker-compose.

## 11. The 30-second pitch (interview-ready)

> "Mem0's `add` is two LLM calls and a reconciling write across a vector store and
> a history table. That's exactly the workload durable execution was built for, so
> I put Restate in front of it: the FastAPI edge does nothing but enqueue an `add`
> workflow and hand back an event ID — same shape as your Platform V3
> `async_mode`. Each LLM call and each DB write is a journaled side effect, so a
> mid-workflow crash doesn't charge OpenRouter twice or leave half-written
> history. The whole API is typed end-to-end: Pydantic models drive the OpenAPI
> spec, `openapi-python-client` regenerates a typed SDK in CI, and ruff +
> pyright-strict gate the merges. One `just up` brings the whole thing up; one
> `just demo` runs the golden path plus a forced-crash chaos test that shows the
> workflow resuming from its journal."
