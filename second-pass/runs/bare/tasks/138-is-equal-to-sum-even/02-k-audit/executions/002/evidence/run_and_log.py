#!/usr/bin/env python3
"""Run one command without a shell and preserve a bounded, exact audit log."""

from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("usage: run_and_log.py LOG COMMAND [ARG ...]")
    log_path = Path(sys.argv[1])
    command = sys.argv[2:]
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )
    output = completed.stdout
    limit = 120_000
    if len(output) > limit:
        output = output[:60_000] + "\n...[bounded log truncation]...\n" + output[-60_000:]
    record = (
        "COMMAND: "
        + shlex.join(command)
        + "\n"
        + output
        + ("" if output.endswith("\n") or not output else "\n")
        + f"EXIT_STATUS: {completed.returncode}\n"
    )
    log_path.write_text(record, encoding="utf-8")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
