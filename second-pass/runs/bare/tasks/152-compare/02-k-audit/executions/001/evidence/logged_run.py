#!/usr/bin/env python3
"""Run one command and preserve a bounded, self-describing audit log."""

from __future__ import annotations

import argparse
import pathlib
import shlex
import subprocess
import sys


MAX_BYTES = 400_000


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    completed = subprocess.run(
        command,
        cwd=args.cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    truncated = len(output) > MAX_BYTES
    if truncated:
        head = MAX_BYTES // 2
        tail = MAX_BYTES - head
        output = (
            output[:head]
            + b"\n\n[... OUTPUT TRUNCATED BY REVIEW HARNESS ...]\n\n"
            + output[-tail:]
        )

    log_path = pathlib.Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"CWD: {pathlib.Path(args.cwd).resolve()}\n"
        f"COMMAND: {shlex.join(command)}\n"
        f"EXIT_STATUS: {completed.returncode}\n"
        f"OUTPUT_BYTES_CAPTURED: {len(output)}\n"
        f"OUTPUT_TRUNCATED: {'yes' if truncated else 'no'}\n"
        "--- OUTPUT ---\n"
    ).encode()
    log_path.write_bytes(header + output)
    sys.stdout.buffer.write(header + output)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
