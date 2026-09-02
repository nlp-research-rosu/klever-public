#!/usr/bin/env python3
"""Run one command and preserve an exact, bounded combined-output record."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


MAX_HEAD = 400_000
MAX_TAIL = 400_000


def main() -> int:
    if len(sys.argv) < 4:
        print("usage: run_logged.py LOG CWD COMMAND [ARG ...]", file=sys.stderr)
        return 2
    log_path = Path(sys.argv[1])
    cwd = Path(sys.argv[2])
    command = sys.argv[3:]
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    print(f"running: {shlex.join(command)}", flush=True)
    with tempfile.NamedTemporaryFile(prefix="audit-command.", dir="/tmp", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        process = subprocess.run(
            command,
            cwd=cwd,
            stdout=tmp,
            stderr=subprocess.STDOUT,
            check=False,
            env=os.environ.copy(),
        )
    data = tmp_path.read_bytes()
    tmp_path.unlink()
    digest = hashlib.sha256(data).hexdigest()
    ended = datetime.now(timezone.utc).isoformat()
    if len(data) <= MAX_HEAD + MAX_TAIL:
        shown = data
        omission = b""
    else:
        omitted = len(data) - MAX_HEAD - MAX_TAIL
        shown = data[:MAX_HEAD] + data[-MAX_TAIL:]
        omission = (
            f"\n[... {omitted} output bytes omitted from this bounded log; "
            f"full-output sha256={digest} ...]\n"
        ).encode()
        shown = data[:MAX_HEAD] + omission + data[-MAX_TAIL:]
    header = (
        f"COMMAND: {shlex.join(command)}\n"
        f"CWD: {cwd.resolve()}\n"
        f"STARTED_UTC: {started}\n"
        f"ENDED_UTC: {ended}\n"
        f"EXIT_STATUS: {process.returncode}\n"
        f"FULL_OUTPUT_BYTES: {len(data)}\n"
        f"FULL_OUTPUT_SHA256: {digest}\n"
        "OUTPUT_BEGIN\n"
    ).encode()
    log_path.write_bytes(header + shown + b"\nOUTPUT_END\n")
    print(
        f"exit={process.returncode} output_bytes={len(data)} "
        f"log={log_path} sha256={digest}",
        flush=True,
    )
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
