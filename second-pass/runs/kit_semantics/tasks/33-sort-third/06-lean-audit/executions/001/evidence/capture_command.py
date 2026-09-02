#!/usr/bin/env python3
"""Run an auditor-selected command and preserve its complete combined output."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("usage: capture_command.py LOG COMMAND [ARG ...]")
    log_path = Path(sys.argv[1])
    command = sys.argv[2:]
    rendered = shlex.join(command)
    selected_cwd = os.environ.get("CAPTURE_CWD")
    result = subprocess.run(
        command,
        cwd=selected_cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
    )
    location = f" (cwd {selected_cwd})" if selected_cwd else ""
    record = (
        f"[cwd]{location or ' inherited'}\n"
        f"$ {rendered}\n"
        f"{result.stdout}"
        f"\n[exit_code] {result.returncode}\n"
    )
    log_path.write_text(record)
    sys.stdout.write(record)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
