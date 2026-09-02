#!/usr/bin/env python3
"""Run one command and preserve a bounded, self-describing audit log."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--max-bytes", type=int, default=200_000)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command[:1] == ["--"]:
        args.command = args.command[1:]
    if not args.command:
        parser.error("missing command")

    env = dict(os.environ)
    profile_bin = str(Path.home() / ".nix-profile" / "bin")
    env["PATH"] = profile_bin + os.pathsep + env.get("PATH", "")
    timed_out = False
    try:
        result = subprocess.run(
            args.command,
            cwd=args.cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=args.timeout,
            check=False,
        )
        output = result.stdout
        status: int | str = result.returncode
    except subprocess.TimeoutExpired as err:
        timed_out = True
        output = (err.stdout or b"") + (err.stderr or b"")
        status = "TIMEOUT"

    omitted = max(0, len(output) - args.max_bytes)
    shown = output[: args.max_bytes]
    lines = [
        f"cwd: {args.cwd}",
        "command: " + shlex.join(args.command),
        f"timeout_seconds: {args.timeout}",
        f"exit_status: {status}",
        f"timed_out: {str(timed_out).lower()}",
        f"captured_bytes: {len(output)}",
        f"omitted_tail_bytes: {omitted}",
        "--- output ---",
    ]
    text = "\n".join(lines).encode() + b"\n" + shown
    if shown and not shown.endswith(b"\n"):
        text += b"\n"
    Path(args.log).write_bytes(text)
    print(Path(args.log).read_text(encoding="utf-8", errors="replace"))
    return 124 if timed_out else int(status)


if __name__ == "__main__":
    raise SystemExit(main())
