#!/usr/bin/env python3
"""Run an argv vector without a shell and record exact merged output and status."""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--cwd")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("missing command")

    completed = subprocess.run(
        command,
        cwd=args.cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )
    record = (
        (f"[cwd] {args.cwd}\n" if args.cwd else "")
        +
        f"$ {shlex.join(command)}\n"
        f"{completed.stdout}"
        f"\n[exit_code] {completed.returncode}\n"
    )
    Path(args.log).write_text(record, encoding="utf-8")
    print(record, end="")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
