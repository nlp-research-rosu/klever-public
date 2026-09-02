#!/usr/bin/env python3
"""Regenerate solution.mpy with the trusted translator and require byte identity."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    solution = Path("/tmp/audit-work/candidate-src/solution.py")
    submitted = Path("/tmp/audit-work/candidate-src/solution.mpy")
    regenerated = Path("/tmp/audit-work/trusted-regenerated-solution.mpy")
    completed = subprocess.run(
        ["python3", "/reference/py2mpy.py", str(solution)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    regenerated.write_bytes(completed.stdout)
    print(f"translator_exit_status={completed.returncode}")
    if completed.stderr:
        print(completed.stderr.decode(errors="replace"))
    print(f"submitted_sha256={sha(submitted)}")
    print(f"regenerated_sha256={sha(regenerated)}")
    print(f"byte_identical={submitted.read_bytes() == regenerated.read_bytes()}")
    assert completed.returncode == 0
    assert submitted.read_bytes() == regenerated.read_bytes()
    print("TRANSLATION_IDENTITY_OK")


if __name__ == "__main__":
    main()
