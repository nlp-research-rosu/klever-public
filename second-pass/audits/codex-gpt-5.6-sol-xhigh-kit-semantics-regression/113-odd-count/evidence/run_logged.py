#!/usr/bin/env python3
"""Run an audit command, preserving a bounded combined log and exact status."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log")
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--limit", type=int, default=200_000)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("missing command after --")

    env = os.environ.copy()
    env["PATH"] = f"/usr/bin:{env.get('PATH', '')}"
    completed = subprocess.run(
        args.command,
        cwd=args.cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    raw = completed.stdout
    if len(raw) > args.limit:
        head = raw[: args.limit // 2]
        tail = raw[-args.limit // 2 :]
        raw = (
            head
            + b"\n... AUDITOR LOG TRUNCATED IN MIDDLE ...\n"
            + tail
        )
    rendered_command = " ".join(
        subprocess.list2cmdline([part]) for part in args.command
    )
    log = (
        f"CWD: {args.cwd}\n"
        f"COMMAND: {rendered_command}\n"
        f"EXIT_STATUS: {completed.returncode}\n"
        "OUTPUT_BEGIN\n"
    ).encode() + raw + b"\nOUTPUT_END\n"
    Path(args.log).write_bytes(log)
    print(log.decode(errors="replace"), end="")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
