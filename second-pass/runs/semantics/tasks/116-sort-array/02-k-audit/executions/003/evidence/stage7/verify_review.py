#!/usr/bin/env python3
"""Check required review structure, final markers, and local evidence links."""

from __future__ import annotations

import re
from pathlib import Path


root = Path("/audit-output")
review = root / "REVIEW.md"
text = review.read_text(encoding="utf-8")
lines = text.splitlines()

expected_tail = ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]
assert lines[-2:] == expected_tail, (lines[-2:], expected_tail)

for stage in range(1, 8):
    assert re.search(rf"^## {stage}\.", text, re.MULTILINE), f"missing stage {stage}"

links = re.findall(r"\]\((evidence/[^)]+)\)", text)
missing = [link for link in links if not (root / link).is_file()]
assert not missing, f"missing linked evidence: {missing}"

print(f"REVIEW_LINES {len(lines)}")
print(f"EVIDENCE_LINKS {len(links)}")
print("MISSING_LINKS 0")
print(f"FINAL_LINE_1 {lines[-2]}")
print(f"FINAL_LINE_2 {lines[-1]}")
