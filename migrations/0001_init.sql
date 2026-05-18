-- Initial schema for the durable Mem0-style memory API.
-- One Postgres holds: vector index (pgvector), audit history, async event ledger.
-- See ARCH.md §4 for the rationale.

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- gen_random_uuid()

-- ---------------------------------------------------------------------------
-- memories: the vector-indexed source of truth for facts about a user/agent.
-- Soft-delete via deleted_at so history reads stay correct.
-- ---------------------------------------------------------------------------
CREATE TABLE memories (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       text        NOT NULL,
    agent_id      text,
    run_id        text,
    content       text        NOT NULL,
    content_hash  text        NOT NULL,                   -- md5(content); skip redundant UPDATEs
    embedding     vector(1536) NOT NULL,
    metadata      jsonb       NOT NULL DEFAULT '{}'::jsonb,
    created_at    timestamptz NOT NULL DEFAULT now(),
    updated_at    timestamptz NOT NULL DEFAULT now(),
    deleted_at    timestamptz
);

CREATE INDEX memories_user_idx
    ON memories (user_id)
    WHERE deleted_at IS NULL;

CREATE INDEX memories_agent_idx
    ON memories (agent_id)
    WHERE deleted_at IS NULL AND agent_id IS NOT NULL;

CREATE INDEX memories_run_idx
    ON memories (run_id)
    WHERE deleted_at IS NULL AND run_id IS NOT NULL;

-- ivfflat needs ANALYZE before it's useful; lists=100 is fine up to ~1M rows.
CREATE INDEX memories_embedding_idx
    ON memories USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- ---------------------------------------------------------------------------
-- memory_history: mirrors mem0's SQLiteManager.history. Append-only.
-- ---------------------------------------------------------------------------
CREATE TABLE memory_history (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id   uuid        NOT NULL,
    old_memory  text,
    new_memory  text,
    event       text        NOT NULL CHECK (event IN ('ADD', 'UPDATE', 'DELETE')),
    actor_id    text,
    role        text,
    created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX memory_history_memory_idx
    ON memory_history (memory_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- add_events: matches mem0 Platform V3 async_mode event lifecycle.
-- The event_id returned to the caller IS the PK here.
-- ---------------------------------------------------------------------------
CREATE TABLE add_events (
    id          uuid PRIMARY KEY,                          -- caller-visible event_id
    user_id     text        NOT NULL,
    status      text        NOT NULL
                CHECK (status IN ('PENDING', 'RUNNING', 'SUCCEEDED', 'FAILED')),
    latency_ms  integer,
    error       text,
    result      jsonb,
    created_at  timestamptz NOT NULL DEFAULT now(),
    updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX add_events_user_idx ON add_events (user_id, created_at DESC);
CREATE INDEX add_events_status_idx ON add_events (status) WHERE status IN ('PENDING', 'RUNNING');
