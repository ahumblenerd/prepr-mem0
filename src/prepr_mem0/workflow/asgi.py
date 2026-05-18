"""ASGI entry point for the Restate worker process.

Run via `uv run uvicorn prepr_mem0.workflow.asgi:app --host 0.0.0.0 --port 9080`.
Restate (in compose) discovers handlers by POSTing to this app's URL via the
admin API at :9070 — see `scripts/register_workflow.sh`.
"""

from __future__ import annotations

import restate

from prepr_mem0.workflow import add_memory_wf, echo_service

app = restate.app(services=[echo_service, add_memory_wf])
