#!/usr/bin/env python3
"""Mechanical completeness checks for REVIEW.md."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


review = Path("/audit-output/REVIEW.md")
text = review.read_text(encoding="utf-8")
lines = text.splitlines()

expected_tail = ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
assert lines[-2:] == expected_tail, lines[-4:]

for stage in range(1, 8):
    assert re.search(rf"^## {stage}\.", text, re.MULTILINE), stage

links = re.findall(r"\]\((evidence/[^)]+)\)", text)
missing = [
    relative
    for relative in links
    if not (Path("/audit-output") / relative).is_file()
]
assert not missing, missing

print(f"bytes={len(text.encode('utf-8'))}")
print(f"sha256={hashlib.sha256(text.encode('utf-8')).hexdigest()}")
print(f"evidence_links={len(links)}")
print("stages=1,2,3,4,5,6,7")
print("tail=VERDICT: FAIL | LEGITIMACY: NOT_LEGIT")
