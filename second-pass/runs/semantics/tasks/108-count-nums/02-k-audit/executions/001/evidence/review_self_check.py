#!/usr/bin/env python3
"""Mechanical completeness checks for the final review artifact."""

from __future__ import annotations

import re
from pathlib import Path


review_path = Path("/audit-output/REVIEW.md")
review = review_path.read_text(encoding="utf-8")
lines = review.splitlines()

expected_tail = ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
if lines[-2:] != expected_tail:
    raise SystemExit(f"bad verdict tail: {lines[-2:]!r}")

stage_headers = re.findall(r"^## ([1-7])\.", review, flags=re.MULTILINE)
if stage_headers != list("1234567"):
    raise SystemExit(f"bad stage headers: {stage_headers!r}")

evidence_links = sorted(set(re.findall(r"\(evidence/([^)]+)\)", review)))
missing = [
    name for name in evidence_links
    if not (Path("/audit-output/evidence") / name).is_file()
]
if missing:
    raise SystemExit(f"missing linked evidence: {missing!r}")

print(f"review={review_path}")
print(f"stage_headers={stage_headers}")
print(f"evidence_links={len(evidence_links)} all_exist=true")
print(f"last_two_lines={lines[-2:]!r}")
