#!/usr/bin/env python3
"""Run one command and preserve a bounded, self-describing command log."""

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
    parser.add_argument("--max-bytes", type=int, default=250_000)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("missing command after --")

    env = os.environ.copy()
    env["PATH"] = f"/home/agent/.nix-profile/bin:{env.get('PATH', '')}"
    completed = subprocess.run(
        command,
        cwd=args.cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    truncated = len(output) > args.max_bytes
    if truncated:
        half = args.max_bytes // 2
        output = (
            output[:half]
            + b"\n\n[... reviewer log truncated in the middle ...]\n\n"
            + output[-half:]
        )

    log = Path(args.log)
    log.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"WORKING_DIRECTORY: {args.cwd}\n"
        f"COMMAND: {shlex.join(command)}\n"
        f"EXIT_STATUS: {completed.returncode}\n"
        f"OUTPUT_BYTES: {len(completed.stdout)}\n"
        f"OUTPUT_TRUNCATED: {str(truncated).lower()}\n"
        "OUTPUT:\n"
    ).encode()
    log.write_bytes(header + output)
    sys.stdout.buffer.write(header + output)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
