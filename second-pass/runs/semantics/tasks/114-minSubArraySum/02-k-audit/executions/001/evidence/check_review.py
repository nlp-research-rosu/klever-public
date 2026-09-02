#!/usr/bin/env python3
"""Mechanical handoff checks for REVIEW.md."""

from __future__ import annotations

import re
from pathlib import Path


review = Path("/audit-output/REVIEW.md")
text = review.read_text(encoding="utf-8")
lines = text.splitlines()
expected = ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]
if lines[-2:] != expected:
    raise SystemExit(f"bad final markers: {lines[-2:]!r}")

references = sorted(set(re.findall(r"evidence/[A-Za-z0-9_.-]+", text)))
missing = [
    reference
    for reference in references
    if not (Path("/audit-output") / reference).exists()
]
if missing:
    raise SystemExit(f"missing evidence references: {missing}")

print(f"review_lines={len(lines)}")
print(f"evidence_references={len(references)}")
print("final_markers_ok=true")
print("all_referenced_evidence_exists=true")
