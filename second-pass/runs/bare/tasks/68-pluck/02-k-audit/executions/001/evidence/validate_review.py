#!/usr/bin/env python3
"""Mechanical final checks for REVIEW.md structure and local citations."""

from __future__ import annotations

import re
from pathlib import Path


review_path = Path("/audit-output/REVIEW.md")
text = review_path.read_text()
lines = text.splitlines()

expected_tail = ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
assert lines[-2:] == expected_tail, (lines[-2:], expected_tail)

stage_headers = re.findall(r"^## ([1-7])\.", text, re.MULTILINE)
assert stage_headers == list("1234567"), stage_headers

targets = re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
missing = []
for target in targets:
    if "://" in target or target.startswith("#"):
        continue
    target_path = (review_path.parent / target).resolve()
    if not target_path.exists():
        missing.append((target, str(target_path)))
assert not missing, missing

print(f"review_bytes={review_path.stat().st_size}")
print(f"stage_headers={stage_headers}")
print(f"local_citations={len(targets)} missing=0")
print(f"final_lines={lines[-2:]}")
