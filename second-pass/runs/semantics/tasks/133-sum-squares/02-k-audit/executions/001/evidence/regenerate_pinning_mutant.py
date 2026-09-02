#!/usr/bin/env python3
"""Regenerate the body-sensitivity mutant from its mutated Python source."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/133-sum-squares-pinning-test")


def main() -> int:
    completed = subprocess.run(
        ["python3", str(ROOT / "py2mpy.py"), str(ROOT / "solution.py")],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (ROOT / "solution.mpy").write_bytes(completed.stdout)
    print(f"translator_exit={completed.returncode}")
    print(f"mpy_sha256={hashlib.sha256(completed.stdout).hexdigest()}")
    print(completed.stdout.decode(errors="replace"))
    if completed.stderr:
        print(completed.stderr.decode(errors="replace"))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
