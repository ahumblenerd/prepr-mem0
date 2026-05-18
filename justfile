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
