#!/usr/bin/env python3
"""Compare the proved loop claim with the installed operational bridge."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def block(path: Path, start_marker: str, end_marker: str) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    body = text[start:end]
    body = re.sub(r"\[priority\(40\)\]", "", body)
    return re.sub(r"\s+", "", body)


claim = block(
    Path("/tmp/audit-work/fresh/spec.k"),
    "claim [loop]:",
    "claim [correct-bracketing]:",
)
bridge = block(
    Path("/tmp/audit-work/fresh/verification-with-loop.k"),
    "rule [loop-lemma]:",
    "endmodule",
)

print(f"claim_sha256={hashlib.sha256(claim.encode()).hexdigest()}")
print(f"bridge_sha256={hashlib.sha256(bridge.encode()).hexdigest()}")
print(f"exact_except_label_whitespace_priority={claim == bridge}")
raise SystemExit(0 if claim == bridge else 1)
