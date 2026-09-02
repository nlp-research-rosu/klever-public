#!/usr/bin/env python3
"""Run one command and preserve its exact argv, cwd, exit status, and output."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    env = os.environ.copy()
    result_kind = "completed"
    try:
        proc = subprocess.run(
            command,
            cwd=args.cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=args.timeout,
            check=False,
        )
        output = proc.stdout
        exit_status = proc.returncode
    except subprocess.TimeoutExpired as err:
        result_kind = "timeout"
        partial = err.stdout or ""
        if isinstance(partial, bytes):
            partial = partial.decode(errors="replace")
        output = partial + f"\nAUDITOR TIMEOUT after {args.timeout} seconds\n"
        exit_status = 124

    log_text = (
        f"COMMAND: {shlex.join(command)}\n"
        f"CWD: {args.cwd}\n"
        f"RESULT_KIND: {result_kind}\n"
        f"EXIT_STATUS: {exit_status}\n"
        "OUTPUT_BEGIN\n"
        f"{output}"
        + ("" if output.endswith("\n") else "\n")
        + "OUTPUT_END\n"
    )
    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(log_text)
    sys.stdout.write(log_text)
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
