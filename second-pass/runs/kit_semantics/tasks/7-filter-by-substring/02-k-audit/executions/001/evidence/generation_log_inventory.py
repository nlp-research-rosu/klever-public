#!/usr/bin/env python3
"""Read the complete plain generation log and inventory notable records."""

from __future__ import annotations

import collections
import hashlib
from pathlib import Path


LOG = Path("/generation/codex-output.log")
MARKERS = (
    "#Top",
    "WarnStuckClaimState",
    "VALIDATED",
    "KPROVE_PASSED",
    "kompile",
    "kprove",
    "krun",
    "apply_patch",
    "timed out",
    "timeout",
    "oom",
)


def main() -> int:
    raw = LOG.read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines()
    print(f"path={LOG}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"bytes={len(raw)}")
    print(f"lines={len(lines)}")
    print(f"nul_bytes={raw.count(bytes([0]))}")
    counts = collections.Counter()
    for line in lines:
        for marker in MARKERS:
            if marker in line:
                counts[marker] += 1
    for marker in MARKERS:
        print(f"marker[{marker}]={counts[marker]}")
    print("first_line=" + (lines[0] if lines else ""))
    print("last_line=" + (lines[-1] if lines else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
