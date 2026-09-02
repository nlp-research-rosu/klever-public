#!/usr/bin/env python3
"""Regenerate solution.mpy with the trusted translator and compare bytes."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/133-sum-squares-audit")
TRANSLATOR = SCRATCH / "py2mpy.py"
SOURCE = SCRATCH / "solution.py"
SUBMITTED = SCRATCH / "solution.mpy"
REGENERATED = SCRATCH / "regenerated-solution.mpy"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    completed = subprocess.run(
        ["python3", str(TRANSLATOR), str(SOURCE)],
        cwd=SCRATCH,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(f"translator_exit={completed.returncode}")
    if completed.stderr:
        print("translator_stderr:")
        print(completed.stderr.decode(errors="replace"))
    REGENERATED.write_bytes(completed.stdout)
    submitted = SUBMITTED.read_bytes()
    print(f"regenerated_sha256={sha256(completed.stdout)}")
    print(f"submitted_sha256={sha256(submitted)}")
    print(f"byte_identical={completed.stdout == submitted}")
    return 0 if completed.returncode == 0 and completed.stdout == submitted else 1


if __name__ == "__main__":
    raise SystemExit(main())
