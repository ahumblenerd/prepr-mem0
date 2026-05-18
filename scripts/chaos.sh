#!/usr/bin/env bash
# Run the chaos-replay test. Assumes the stack is up (db + restate + api).
set -euo pipefail

cd "$(dirname "$0")/.."

# Ensure fastapi process exists; chaos test orchestrates worker itself.
if ! curl -fsS http://localhost:8000/healthz > /dev/null 2>&1; then
    echo "FastAPI not running on :8000 — start with 'just api' first" >&2
    exit 1
fi

# Make sure the chaos test can manage the worker freely.
if [ -f .worker.pid ]; then
    just kill-worker || true
fi

exec uv run pytest tests/chaos/test_resume_after_crash.py \
    -m chaos --no-cov -v -s "$@"
