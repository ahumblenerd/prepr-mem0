"""Opt-in chaos hook the workflow can plant between steps.

Set `CHAOS_AT=<hook>` in the worker env and `maybe_crash("<hook>")` will
hard-exit the process. Used by Phase 6's chaos test to prove Restate
resumes from its journal after the worker dies mid-flight.

`os._exit` (not `sys.exit`) — `sys.exit` raises `SystemExit`, which the
Restate SDK can catch and convert into a FAILED workflow, defeating the
test. We want the process to vanish.
"""

from __future__ import annotations

import os


def maybe_crash(hook: str) -> None:
    """Hard-exit the process if `CHAOS_AT` matches `hook`."""
    if os.environ.get("CHAOS_AT") == hook:
        # Unset so the restarted worker doesn't crash on the same hook again.
        os.environ.pop("CHAOS_AT", None)
        os._exit(1)
