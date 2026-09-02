#!/usr/bin/env python3
"""Translate one Python probe with the mounted trusted translator."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--translator", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    completed = subprocess.run(
        ["python3", args.translator, args.source],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.stderr:
        print(completed.stderr.decode("utf-8", errors="replace"))
    Path(args.output).write_bytes(completed.stdout)
    print(f"translator_exit={completed.returncode}")
    print(f"generated_bytes={len(completed.stdout)} output={args.output}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
