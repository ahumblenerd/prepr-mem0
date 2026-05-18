"""Smoke-test Restate service. Proves the runtime is wired before we build
the real `add_memory` workflow in Phase 5."""

from __future__ import annotations

import restate

echo_service = restate.Service("memory")


@echo_service.handler(name="echo")
async def echo(_ctx: restate.Context, message: str) -> str:
    return message
