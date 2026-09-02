#!/usr/bin/env python3
"""Read an entire untrusted generation log and emit bounded claim evidence."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    args = parser.parse_args()

    raw = args.log.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    needles = (
        "#Top",
        "WarnStuckClaimState",
        "KPROVE_PASSED",
        "Incomplete work",
        "Gate A",
        "mismatch",
        "timed out",
    )
    print(f"path: {args.log}")
    print(f"sha256: {hashlib.sha256(raw).hexdigest()}")
    print(f"bytes: {len(raw)}")
    print(f"lines: {len(lines)}")
    for needle in needles:
        print(f"count[{needle!r}]: {text.count(needle)}")
    print("last 80 lines (untrusted claims, bounded):")
    print("\n".join(lines[-80:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
