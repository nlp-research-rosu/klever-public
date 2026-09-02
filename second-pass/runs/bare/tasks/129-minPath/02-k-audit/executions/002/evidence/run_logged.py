#!/usr/bin/env python3
"""Run one command and preserve an exact, bounded combined-output transcript."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import shlex
import subprocess
import sys
from pathlib import Path


MAX_LOG_BYTES = 500_000


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    started = dt.datetime.now(dt.timezone.utc)
    timed_out = False
    try:
        completed = subprocess.run(
            command,
            cwd=args.cwd,
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=args.timeout,
            check=False,
        )
        returncode = completed.returncode
        output = completed.stdout
    except subprocess.TimeoutExpired as error:
        timed_out = True
        returncode = 124
        output = (error.stdout or b"") + (error.stderr or b"")
    ended = dt.datetime.now(dt.timezone.utc)

    truncated = len(output) > MAX_LOG_BYTES
    if truncated:
        half = MAX_LOG_BYTES // 2
        output_for_log = (
            output[:half]
            + b"\n\n[... reviewer log truncated in the middle ...]\n\n"
            + output[-half:]
        )
    else:
        output_for_log = output

    header = "\n".join(
        [
            f"command: {shlex.join(command)}",
            f"cwd: {args.cwd.resolve()}",
            f"started_utc: {started.isoformat()}",
            f"ended_utc: {ended.isoformat()}",
            f"timeout_seconds: {args.timeout}",
            f"timed_out: {str(timed_out).lower()}",
            f"exit_status: {returncode}",
            f"captured_output_bytes: {len(output)}",
            f"log_middle_truncated: {str(truncated).lower()}",
            "",
            "----- combined stdout/stderr -----",
            "",
        ]
    ).encode()
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.log.write_bytes(header + output_for_log)

    sys.stdout.buffer.write(output)
    sys.stdout.flush()
    print(f"\n[run_logged exit_status={returncode} log={args.log}]", file=sys.stderr)
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
