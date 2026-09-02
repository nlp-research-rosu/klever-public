#!/usr/bin/env python3
"""Run one command and preserve a bounded, auditable combined-output log."""

from __future__ import annotations

import datetime
import pathlib
import shlex
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: command_runner.py LOG COMMAND [ARG ...]", file=sys.stderr)
        return 2

    log_path = pathlib.Path(sys.argv[1])
    command = sys.argv[2:]
    started = datetime.datetime.now(datetime.timezone.utc)
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
    )
    finished = datetime.datetime.now(datetime.timezone.utc)
    output = result.stdout
    max_chars = 200_000
    if len(output) > max_chars:
        half = max_chars // 2
        output = (
            output[:half]
            + "\n...[bounded log: middle omitted]...\n"
            + output[-half:]
        )

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "\n".join(
            [
                f"START_UTC: {started.isoformat()}",
                f"WORKDIR: {pathlib.Path.cwd()}",
                "COMMAND: " + shlex.join(command),
                f"EXIT_STATUS: {result.returncode}",
                f"FINISH_UTC: {finished.isoformat()}",
                "OUTPUT:",
                output,
            ]
        ),
        encoding="utf-8",
    )
    sys.stdout.write(output)
    print(f"\n[exit {result.returncode}; log {log_path}]")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
