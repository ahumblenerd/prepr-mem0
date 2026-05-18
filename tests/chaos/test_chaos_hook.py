"""Tests for the in-process chaos hook used by Phase 6's resume test."""

from __future__ import annotations

import subprocess
import sys
import textwrap


def test_chaos_hook_exits_when_env_set():
    code = textwrap.dedent(
        """
        import os, sys
        sys.path.insert(0, "src")
        os.environ["CHAOS_AT"] = "extract"
        from prepr_mem0.workflow.chaos import maybe_crash
        maybe_crash("extract")
        # Should not reach here.
        sys.exit(0)
        """
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        timeout=5,
    )
    assert proc.returncode == 1, (
        f"expected hard exit, got {proc.returncode}; stderr={proc.stderr!r}"
    )


def test_chaos_hook_noop_when_env_unset():
    code = textwrap.dedent(
        """
        import os, sys
        sys.path.insert(0, "src")
        os.environ.pop("CHAOS_AT", None)
        from prepr_mem0.workflow.chaos import maybe_crash
        maybe_crash("extract")
        sys.exit(0)
        """
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        timeout=5,
    )
    assert proc.returncode == 0, f"expected clean exit; stderr={proc.stderr!r}"


def test_chaos_hook_noop_when_hook_name_mismatches():
    code = textwrap.dedent(
        """
        import os, sys
        sys.path.insert(0, "src")
        os.environ["CHAOS_AT"] = "decide"  # different hook name
        from prepr_mem0.workflow.chaos import maybe_crash
        maybe_crash("extract")
        sys.exit(0)
        """
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        timeout=5,
    )
    assert proc.returncode == 0
