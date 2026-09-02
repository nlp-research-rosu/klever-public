#!/usr/bin/env python3
"""Regenerate solution.mpy with the trusted translator and require byte identity."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    source = Path("/tmp/audit-work/source/solution.py")
    submitted = Path("/candidate/solution.mpy")
    regenerated = Path("/tmp/audit-work/source/solution.regenerated.mpy")
    completed = subprocess.run(
        ["python3", "/reference/py2mpy.py", str(source)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    regenerated.write_bytes(completed.stdout)
    print(f"translator_exit={completed.returncode}")
    print(f"translator_stderr={completed.stderr.decode(errors='replace')!r}")
    print(f"submitted_sha256={sha256(submitted.read_bytes())}")
    print(f"regenerated_sha256={sha256(completed.stdout)}")
    print(f"byte_identity={completed.stdout == submitted.read_bytes()}")
    return 0 if completed.returncode == 0 and completed.stdout == submitted.read_bytes() else 1


if __name__ == "__main__":
    raise SystemExit(main())
