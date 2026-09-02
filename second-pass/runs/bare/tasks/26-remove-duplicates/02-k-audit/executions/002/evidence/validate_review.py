#!/usr/bin/env python3
"""Final structural checks for REVIEW.md and its local evidence references."""

from __future__ import annotations

import re
from pathlib import Path


review = Path("/audit-output/REVIEW.md")
text = review.read_text()
lines = text.splitlines()
expected = ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
print(f"review_bytes={review.stat().st_size}")
print(f"review_lines={len(lines)}")
print(f"final_lines={lines[-2:]!r}")
print(f"final_lines_exact={lines[-2:] == expected}")

references = sorted(set(re.findall(r"`(evidence/[^`]+)`", text)))
missing = [
    relative
    for relative in references
    if not (Path("/audit-output") / relative).exists()
]
print(f"evidence_reference_count={len(references)}")
print(f"missing_evidence_references={missing!r}")

if lines[-2:] != expected or missing:
    raise SystemExit(1)
