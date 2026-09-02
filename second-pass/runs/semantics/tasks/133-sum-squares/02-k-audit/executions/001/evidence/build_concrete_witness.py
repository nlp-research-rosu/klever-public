#!/usr/bin/env python3
"""Translate the reviewer-authored concrete witness with the trusted translator."""

from __future__ import annotations

import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/133-sum-squares-audit")
SOURCE = Path("/audit-output/evidence/concrete_witness.py")
OUTPUT = SCRATCH / "concrete-witness.mpy"


def main() -> int:
    completed = subprocess.run(
        ["python3", str(SCRATCH / "py2mpy.py"), str(SOURCE)],
        cwd=SCRATCH,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    OUTPUT.write_bytes(completed.stdout)
    print(f"translator_exit={completed.returncode}")
    print(f"output={OUTPUT}")
    print(f"output_bytes={len(completed.stdout)}")
    if completed.stderr:
        print(completed.stderr.decode(errors="replace"))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
