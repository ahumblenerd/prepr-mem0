#!/usr/bin/env bash
# Register the worker process with the running Restate runtime.
# Restate (in docker) reaches the host worker via host.docker.internal:9080.

set -euo pipefail

ADMIN_URL="${RESTATE_ADMIN_URL:-http://localhost:9070}"
WORKER_URL="${WORKER_URL:-http://host.docker.internal:9080}"

echo "registering $WORKER_URL with $ADMIN_URL..."
curl -fsS -X POST "$ADMIN_URL/deployments" \
    -H 'content-type: application/json' \
    -d "{\"uri\":\"$WORKER_URL\",\"use_http_11\":true,\"force\":true}"
echo
