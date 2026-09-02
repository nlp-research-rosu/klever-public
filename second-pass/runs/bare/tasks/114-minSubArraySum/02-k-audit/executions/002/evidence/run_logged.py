#!/usr/bin/env python3
"""Run one command, preserving its exact argv, cwd, merged output, and status."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--cwd", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("missing command after --")

    environment = os.environ.copy()
    nix_bin = str(Path.home() / ".nix-profile" / "bin")
    environment["PATH"] = nix_bin + os.pathsep + environment.get("PATH", "")
    try:
        completed = subprocess.run(
            command,
            cwd=args.cwd,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=args.timeout,
            check=False,
        )
        status = completed.returncode
        output = completed.stdout
        timed_out = False
    except subprocess.TimeoutExpired as error:
        status = 124
        output = (error.stdout or "") + (error.stderr or "")
        timed_out = True

    record = (
        f"CWD: {args.cwd}\n"
        f"COMMAND_ARGV: {command!r}\n"
        f"COMMAND_SHELL: {shlex.join(command)}\n"
        f"TIMEOUT_SECONDS: {args.timeout}\n"
        f"--- OUTPUT ---\n{output}"
        f"{'' if output.endswith(chr(10)) or not output else chr(10)}"
        f"--- RESULT ---\nEXIT_STATUS: {status}\n"
        f"TIMED_OUT: {str(timed_out).lower()}\n"
    )
    args.log.write_text(record, encoding="utf-8")
    print(record, end="")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
