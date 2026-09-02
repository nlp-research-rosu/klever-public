#!/usr/bin/env python3
"""Read and summarize the complete untrusted generation console record."""

from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path


path = Path("/generation-evidence/codex-output.log")
data = path.read_bytes()
text = data.decode("utf-8", errors="replace")
lines = text.splitlines()
patterns = (
    "#Top",
    "WarnStuckClaimState",
    "[Error]",
    "apply_patch",
    "exec_command",
    "kprove",
    "kompile",
    "RESULT:",
)
counts = Counter()
for line in lines:
    for pattern in patterns:
        if pattern in line:
            counts[pattern] += 1

nonempty = [line for line in lines if line.strip()]
print("SHA256=", hashlib.sha256(data).hexdigest())
print("BYTE_COUNT=", len(data))
print("LINE_COUNT=", len(lines))
print("PATTERN_LINE_COUNTS=", dict(counts))
print("FIRST_NONEMPTY=", nonempty[0][:500] if nonempty else "")
print("LAST_NONEMPTY=", nonempty[-1][-500:] if nonempty else "")
