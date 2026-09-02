#!/usr/bin/env python3
"""Run one command and preserve its exact combined output and exit status."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("usage: run_logged.py OUTPUT COMMAND [ARG ...]")
    output_path = Path(sys.argv[1])
    command = sys.argv[2:]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
    )
    record = {
        "command": command,
        "cwd": str(Path.cwd()),
        "exit_code": result.returncode,
        "output": result.stdout,
    }
    output_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    sys.stdout.write(result.stdout)
    print(f"[exit_code={result.returncode}]")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
