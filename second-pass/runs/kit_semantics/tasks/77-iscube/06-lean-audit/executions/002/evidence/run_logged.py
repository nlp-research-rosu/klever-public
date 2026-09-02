#!/usr/bin/env python3
"""Run one command without a shell and preserve its exact combined output."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    completed = subprocess.run(
        command,
        cwd=args.cwd,
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )
    record = (
        f"CWD: {args.cwd}\n"
        f"COMMAND: {shlex.join(command)}\n"
        f"EXIT: {completed.returncode}\n"
        "OUTPUT:\n"
        f"{completed.stdout}"
    )
    Path(args.log).write_text(record, encoding="utf-8")
    sys.stdout.write(record)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
