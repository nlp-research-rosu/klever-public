#!/usr/bin/env python3
"""Read the complete untrusted generation log and summarize proof-related claims."""

from __future__ import annotations

import hashlib
from pathlib import Path


path = Path("/generation-evidence/codex-output.log")
raw = path.read_bytes()
text = raw.decode("utf-8", errors="replace")
lines = text.splitlines()
needles = (
    "kprove",
    "#Top",
    "WarnStuckClaimState",
    "RESULT:",
    "KPROVE_PASSED",
    "kompile",
    "krun solution.mpy",
)
selected = [
    (number, line)
    for number, line in enumerate(lines, 1)
    if any(needle in line for needle in needles)
]

print(f"bytes={len(raw)}")
print(f"lines={len(lines)}")
print(f"sha256={hashlib.sha256(raw).hexdigest()}")
print(f"selected_lines={len(selected)}")
for number, line in selected:
    print(f"{number}: {line[:800]}")
