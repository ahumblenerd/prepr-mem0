"""The headline chaos test: kill worker mid-flight, prove Restate replays.

Choreography:

1. Wipe `/tmp/openrouter_calls.jsonl`.
2. Start the fake OpenRouter HTTP server on :9999 (durable call counter
   that survives the worker dying).
3. Start the worker with `CHAOS_AT=after_extract_facts` and
   `OPENROUTER_BASE_URL=http://host.docker.internal:9999` so it can
   actually reach the fake server from inside Restate's resolution.
4. POST `/v1/memories` — the workflow runs extract_facts (1st call to
   fake server), then the chaos hook hard-exits the worker.
5. Restart the worker WITHOUT `CHAOS_AT`.
6. Poll `/v1/events/{id}` until SUCCEEDED. The worker replays from
   Restate's journal: extract_facts returns its cached value (no 2nd
   call), then decide_actions makes a fresh call (the 2nd call total).
7. Assert exactly 2 lines in the jsonl file. If extract had been
   re-executed, count would be 3.

Requires `just up` to have run (db + restate + worker + register).
Marked `@pytest.mark.chaos` so it's excluded from `just check`.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest

pytestmark = pytest.mark.chaos

REPO_ROOT = Path(__file__).resolve().parents[2]
CALLS_PATH = Path("/tmp/openrouter_calls.jsonl")  # noqa: S108
WORKER_PID = REPO_ROOT / ".worker.pid"
API_BASE = "http://localhost:8000"
FAKE_OPENROUTER_PORT = 9999


def _kill_pid_file(pid_file: Path) -> None:
    if not pid_file.exists():
        return
    pid = int(pid_file.read_text().strip())
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    pid_file.unlink(missing_ok=True)
    # Wait a tick for the port to free.
    time.sleep(0.5)


def _start_worker(extra_env: dict[str, str]) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    env.update(extra_env)
    log = (REPO_ROOT / ".worker.log").open("ab")
    proc = subprocess.Popen(
        [
            "uv",
            "run",
            "uvicorn",
            "prepr_mem0.workflow.asgi:app",
            "--host",
            "0.0.0.0",  # noqa: S104
            "--port",
            "9080",
        ],
        cwd=str(REPO_ROOT),
        env=env,
        stdout=log,
        stderr=log,
    )
    WORKER_PID.write_text(str(proc.pid))
    # Wait until uvicorn binds the port.
    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            httpx.get("http://localhost:9080/discover", timeout=0.5)
            return proc
        except Exception:
            time.sleep(0.2)
    msg = "worker failed to come up within 15s"
    raise RuntimeError(msg)


def _start_fake_openrouter() -> subprocess.Popen[bytes]:
    log = (REPO_ROOT / ".fake_openrouter.log").open("ab")
    proc = subprocess.Popen(
        [
            "uv",
            "run",
            "uvicorn",
            "tests.chaos.fake_openrouter:app",
            "--host",
            "0.0.0.0",  # noqa: S104
            "--port",
            str(FAKE_OPENROUTER_PORT),
        ],
        cwd=str(REPO_ROOT),
        stdout=log,
        stderr=log,
    )
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            r = httpx.get(f"http://localhost:{FAKE_OPENROUTER_PORT}/healthz", timeout=0.5)
            if r.status_code == 200:
                return proc
        except Exception:
            time.sleep(0.2)
    proc.kill()
    msg = "fake_openrouter failed to come up within 10s"
    raise RuntimeError(msg)


def _wait_for_dead_worker(pid: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            os.kill(pid, 0)  # signal 0 = "is it alive?"
        except ProcessLookupError:
            return True
        time.sleep(0.2)
    return False


def _poll_event(event_id: str, timeout: float = 60.0) -> dict:
    deadline = time.time() + timeout
    last: dict = {}
    while time.time() < deadline:
        try:
            r = httpx.get(f"{API_BASE}/v1/events/{event_id}", timeout=2.0)
            if r.status_code == 200:
                last = r.json()
                if last.get("status") in {"SUCCEEDED", "FAILED"}:
                    return last
        except Exception:
            pass
        time.sleep(0.5)
    msg = f"event did not reach terminal state in {timeout}s; last={last}"
    raise AssertionError(msg)


def test_resume_after_crash():
    # 0. Sanity — stack must be running.
    try:
        httpx.get(f"{API_BASE}/healthz", timeout=1.0).raise_for_status()
    except Exception as exc:
        pytest.skip(f"FastAPI not running; run `just up && just api` first ({exc})")

    # 1. Clean state.
    CALLS_PATH.unlink(missing_ok=True)
    _kill_pid_file(WORKER_PID)

    fake = _start_fake_openrouter()
    crashy_worker: subprocess.Popen[bytes] | None = None
    healthy_worker: subprocess.Popen[bytes] | None = None
    try:
        # 2. Boot worker with the chaos env.
        crashy_env = {
            "CHAOS_AT": "after_extract_facts",
            "OPENROUTER_API_KEY": "fake-key",
            "OPENROUTER_BASE_URL": f"http://host.docker.internal:{FAKE_OPENROUTER_PORT}",
        }
        crashy_worker = _start_worker(crashy_env)

        # 3. Fire the workflow.
        r = httpx.post(
            f"{API_BASE}/v1/memories",
            json={
                "user_id": f"chaos-{int(time.time())}",
                "messages": [{"role": "user", "content": "My name is Alice and I like tea."}],
            },
            timeout=5.0,
        )
        assert r.status_code == 202, r.text
        event_id = r.json()["event_id"]
        assert r.json()["status"] == "PENDING"

        # 4. Wait until the worker dies (chaos hook should fire shortly after extract).
        assert _wait_for_dead_worker(crashy_worker.pid, timeout=20.0), (
            "worker did not crash within 20s — chaos hook misfire?"
        )
        WORKER_PID.unlink(missing_ok=True)

        # 5. Restart worker WITHOUT chaos. Same OPENROUTER_BASE_URL.
        clean_env = {
            "OPENROUTER_API_KEY": "fake-key",
            "OPENROUTER_BASE_URL": f"http://host.docker.internal:{FAKE_OPENROUTER_PORT}",
        }
        healthy_worker = _start_worker(clean_env)

        # 6. Poll until terminal.
        final = _poll_event(event_id, timeout=60.0)
        assert final["status"] == "SUCCEEDED", f"workflow did not recover: {final}"
        assert final["result"], "expected applied actions"

        # 7. The headline check: exactly 2 OpenRouter calls — extract + decide.
        lines = CALLS_PATH.read_text().strip().splitlines() if CALLS_PATH.exists() else []
        assert len(lines) == 2, (
            f"expected exactly 2 OpenRouter calls (extract + decide); "
            f"got {len(lines)}. If 3, extract was re-executed instead of replayed."
        )
        sys.stdout.write(f"extract_facts + decide_actions calls: {len(lines)} OK\n")
    finally:
        if healthy_worker is not None:
            healthy_worker.terminate()
            healthy_worker.wait(timeout=5)
        elif crashy_worker is not None and crashy_worker.poll() is None:
            crashy_worker.terminate()
            crashy_worker.wait(timeout=5)
        fake.terminate()
        fake.wait(timeout=5)
        WORKER_PID.unlink(missing_ok=True)
