#!/usr/bin/env python3
"""Regenerate the MPY program with the trusted translator and compare bytes."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--translator", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--submitted", required=True)
    parser.add_argument("--regenerated", required=True)
    args = parser.parse_args()

    completed = subprocess.run(
        ["python3", args.translator, args.source],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    print(f"translator_exit={completed.returncode}")
    if completed.stderr:
        print("translator_stderr:")
        print(completed.stderr.decode("utf-8", errors="replace"))
    regenerated_path = Path(args.regenerated)
    regenerated_path.write_bytes(completed.stdout)
    submitted = Path(args.submitted).read_bytes()
    print(
        f"submitted_bytes={len(submitted)} "
        f"submitted_sha256={sha256(submitted)}"
    )
    print(
        f"regenerated_bytes={len(completed.stdout)} "
        f"regenerated_sha256={sha256(completed.stdout)}"
    )
    print(f"byte_identity={submitted == completed.stdout}")
    return 0 if completed.returncode == 0 and submitted == completed.stdout else 1


if __name__ == "__main__":
    raise SystemExit(main())
