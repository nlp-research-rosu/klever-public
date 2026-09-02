#!/usr/bin/env python3
"""Run one command and preserve a bounded combined-output audit log."""

from __future__ import annotations

import datetime as dt
import os
import pathlib
import shlex
import subprocess
import sys


LIMIT = 300_000


def main() -> int:
    if len(sys.argv) < 4 or sys.argv[2] != "--":
        print("usage: run_logged.py LOG -- COMMAND [ARG ...]", file=sys.stderr)
        return 2

    log_path = pathlib.Path(sys.argv[1])
    command = sys.argv[3:]
    started = dt.datetime.now(dt.timezone.utc)
    completed = subprocess.run(
        command,
        cwd=os.getcwd(),
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    if len(output) > LIMIT:
        half = LIMIT // 2
        removed = len(output) - (2 * half)
        output = (
            output[:half]
            + f"\n...[bounded log omitted {removed} bytes]...\n".encode()
            + output[-half:]
        )
    ended = dt.datetime.now(dt.timezone.utc)
    header = (
        f"COMMAND: {shlex.join(command)}\n"
        f"CWD: {os.getcwd()}\n"
        f"START_UTC: {started.isoformat()}\n"
        f"END_UTC: {ended.isoformat()}\n"
        f"EXIT_STATUS: {completed.returncode}\n"
        "OUTPUT:\n"
    ).encode()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_bytes(header + output)
    sys.stdout.buffer.write(output)
    print(f"\n[exit {completed.returncode}; log {log_path}]", file=sys.stderr)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
