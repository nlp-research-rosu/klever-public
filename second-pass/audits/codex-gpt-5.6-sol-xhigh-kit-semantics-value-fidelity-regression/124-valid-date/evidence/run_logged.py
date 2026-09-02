#!/usr/bin/env python3
"""Run one argv-style command and preserve a bounded, status-bearing log."""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import sys


MAX_BYTES = 200_000
HEAD_BYTES = 120_000
TAIL_BYTES = 80_000


def main() -> int:
    if len(sys.argv) < 4 or sys.argv[2] != "--":
        print("usage: run_logged.py LOG -- COMMAND [ARG ...]", file=sys.stderr)
        return 2
    log_path = Path(sys.argv[1])
    command = sys.argv[3:]
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
        check=False,
    )
    output = completed.stdout
    if len(output) > MAX_BYTES:
        omitted = len(output) - HEAD_BYTES - TAIL_BYTES
        output = (
            output[:HEAD_BYTES]
            + f"\n[... {omitted} output bytes omitted by audit logger ...]\n".encode()
            + output[-TAIL_BYTES:]
        )
    header = (
        f"COMMAND: {shlex.join(command)}\n"
        f"WORKDIR: {Path.cwd()}\n"
    ).encode()
    footer = f"\nEXIT_STATUS: {completed.returncode}\n".encode()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_bytes(header + output + footer)
    sys.stdout.buffer.write(output)
    if output and not output.endswith(b"\n"):
        sys.stdout.buffer.write(b"\n")
    print(f"EXIT_STATUS: {completed.returncode}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
