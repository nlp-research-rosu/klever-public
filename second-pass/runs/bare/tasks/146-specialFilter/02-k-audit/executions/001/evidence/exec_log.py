#!/usr/bin/env python3
"""Run one audit command and preserve a bounded, self-describing log."""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import sys
from datetime import datetime, timezone


LIMIT = 240_000


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: exec_log.py LOGFILE COMMAND [ARG ...]", file=sys.stderr)
        return 2

    log_path = Path(sys.argv[1])
    command = sys.argv[2:]
    started = datetime.now(timezone.utc)
    result = subprocess.run(
        command,
        cwd=os.getcwd(),
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
    )
    finished = datetime.now(timezone.utc)
    output = result.stdout
    truncated = len(output.encode("utf-8")) > LIMIT
    if truncated:
        encoded = output.encode("utf-8")[:LIMIT]
        output = encoded.decode("utf-8", errors="replace")
        output += "\n[LOG TRUNCATED AT 240000 BYTES]\n"

    record = [
        f"started_utc: {started.isoformat()}",
        f"cwd: {os.getcwd()}",
        f"command: {shlex.join(command)}",
        f"exit_status: {result.returncode}",
        f"finished_utc: {finished.isoformat()}",
        f"output_truncated: {'yes' if truncated else 'no'}",
        "--- output ---",
        output,
    ]
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(record), encoding="utf-8")
    sys.stdout.write(output)
    print(f"[exec_log exit={result.returncode} log={log_path}]", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
