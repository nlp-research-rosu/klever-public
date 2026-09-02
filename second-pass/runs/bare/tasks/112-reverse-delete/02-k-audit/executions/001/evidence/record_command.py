#!/usr/bin/env python3
"""Run one command and preserve a bounded, self-describing audit log."""

from __future__ import annotations

import argparse
import datetime
import os
import shlex
import subprocess
import sys


def bounded(data: bytes, limit: int) -> bytes:
    if len(data) <= limit:
        return data
    half = limit // 2
    marker = (
        b"\n\n[AUDIT LOG TRUNCATED: "
        + str(len(data) - 2 * half).encode("ascii")
        + b" BYTES OMITTED]\n\n"
    )
    return data[:half] + marker + data[-half:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--max-bytes", type=int, default=400_000)
    parser.add_argument("--stdout-file")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    timed_out = False
    try:
        result = subprocess.run(
            command,
            cwd=args.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.timeout,
            check=False,
        )
        status = result.returncode
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        status = 124
        stdout = error.stdout or b""
        stderr = error.stderr or b""

    if args.stdout_file is not None:
        with open(args.stdout_file, "wb") as stream:
            stream.write(stdout)

    command_text = shlex.join(command)
    header = (
        f"COMMAND: {command_text}\n"
        f"CWD: {os.path.abspath(args.cwd)}\n"
        f"STARTED_UTC: {started}\n"
        f"TIMEOUT_SECONDS: {args.timeout}\n"
        f"TIMED_OUT: {str(timed_out).lower()}\n"
        f"EXIT_STATUS: {status}\n"
        f"STDOUT_BYTES: {len(stdout)}\n"
        f"STDERR_BYTES: {len(stderr)}\n"
        "----- STDOUT -----\n"
    ).encode("utf-8")
    body = bounded(stdout, args.max_bytes)
    middle = b"\n----- STDERR -----\n"
    tail = bounded(stderr, args.max_bytes)
    with open(args.log, "wb") as stream:
        stream.write(header)
        stream.write(body)
        stream.write(middle)
        stream.write(tail)
        stream.write(b"\n----- END -----\n")

    sys.stdout.buffer.write(stdout)
    sys.stderr.buffer.write(stderr)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
