# Justfile — single entry point for every demoable + agent-verifiable step.
# Run `just` (no args) to list targets.

set shell := ["bash", "-cu"]
set dotenv-load := true

default:
    @just --list

# --- Phase 0: quality gate ---------------------------------------------------

# Install / sync the dev environment.
sync:
    uv sync

# Format in place. Run before commit.
fmt:
    uv run ruff format .
    uv run ruff check --fix .

# Quality gate. Fails the build on any violation. Mirrors CI exactly.
check: lint typecheck security test

lint:
    uv run ruff format --check .
    uv run ruff check .

typecheck:
    uv run pyright

security:
    uv run bandit -q -c pyproject.toml -r src

test:
    uv run pytest

# Install the pre-commit git hook (one-time per clone).
hooks:
    uv run pre-commit install

# Run pre-commit across every file (CI parity).
hooks-all:
    uv run pre-commit run --all-files

# --- Phase 1: Postgres + pgvector --------------------------------------------

DB_URL := "postgresql://prepr:prepr@localhost:5433/prepr"

# Bring the database up and wait until healthy.
up-db:
    docker compose up -d db
    @echo "waiting for postgres…"
    @until docker compose exec -T db pg_isready -U prepr -d prepr > /dev/null 2>&1; do sleep 0.2; done
    @echo "postgres ready"

# Stop and remove the database container (data is tmpfs, so it goes too).
down-db:
    docker compose down -v

# Apply every SQL file in migrations/ in lexical order. Idempotent only on empty DB.
migrate:
    @./scripts/migrate.sh

# Open an interactive psql shell.
db-shell:
    docker compose exec -it db psql -U prepr -d prepr

# Run a one-shot SQL string:  just db-sql "SELECT 1;"
db-sql SQL:
    @docker compose exec -T db psql -U prepr -d prepr -tAc {{quote(SQL)}}

# Phase 1 smoke: pgvector loaded, all three tables present.
db-smoke:
    @echo "--- extensions ---"
    @just db-sql "SELECT extname FROM pg_extension WHERE extname IN ('vector','pgcrypto') ORDER BY extname;"
    @echo "--- tables ---"
    @just db-sql "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;"

# --- Phase 3: Restate runtime + workflow worker -----------------------------

# Bring up Postgres + Restate. Wait until both are healthy.
up-infra:
    docker compose up -d db restate
    @echo "waiting for postgres…"
    @until docker compose exec -T db pg_isready -U prepr -d prepr > /dev/null 2>&1; do sleep 0.2; done
    @echo "waiting for restate…"
    @until curl -fsS http://localhost:9070/health > /dev/null 2>&1; do sleep 0.2; done
    @echo "infra ready"

# Tear it all down.
down:
    docker compose down -v
    -@pkill -f 'prepr_mem0.workflow.asgi' 2>/dev/null || true
    -@pkill -f 'prepr_mem0.api' 2>/dev/null || true
    -@rm -f .worker.pid .api.pid

# Run the Restate worker in the background. PID written to .worker.pid.
worker:
    @if [ -f .worker.pid ] && kill -0 $(cat .worker.pid) 2>/dev/null; then \
        echo "worker already running (pid $(cat .worker.pid))"; \
    else \
        nohup uv run uvicorn prepr_mem0.workflow.asgi:app --host 0.0.0.0 --port 9080 \
            > .worker.log 2>&1 & \
        echo $$! > .worker.pid; \
        echo "worker started (pid $$(cat .worker.pid)); log at .worker.log"; \
        until curl -fsS http://localhost:9080/health > /dev/null 2>&1 || \
              curl -fsS http://localhost:9080/discover > /dev/null 2>&1; do sleep 0.2; done; \
        echo "worker ready"; \
    fi

# Kill the worker (used by chaos tests).
kill-worker:
    @if [ -f .worker.pid ]; then kill $(cat .worker.pid) 2>/dev/null || true; rm .worker.pid; echo "worker killed"; else echo "no worker pid"; fi

# Register the worker with Restate.
register:
    @./scripts/register_workflow.sh

# Full bring-up: infra + migrations + worker + register. Idempotent on the
# registration step (Restate returns 200 with the same deployment id).
up: up-infra migrate worker register
    @echo "stack up — ingress at :8080, admin at :9070, api at :8000 (separate: just api)"

# Run the FastAPI app on :8000 in the background.
api:
    @if [ -f .api.pid ] && kill -0 $(cat .api.pid) 2>/dev/null; then \
        echo "api already running (pid $(cat .api.pid))"; \
    else \
        nohup uv run uvicorn prepr_mem0.api:app --host 0.0.0.0 --port 8000 \
            > .api.log 2>&1 & \
        echo $$! > .api.pid; \
        until curl -fsS http://localhost:8000/healthz > /dev/null 2>&1; do sleep 0.2; done; \
        echo "api ready (pid $$(cat .api.pid))"; \
    fi

kill-api:
    @if [ -f .api.pid ]; then kill $(cat .api.pid) 2>/dev/null || true; rm .api.pid; echo "api killed"; fi
