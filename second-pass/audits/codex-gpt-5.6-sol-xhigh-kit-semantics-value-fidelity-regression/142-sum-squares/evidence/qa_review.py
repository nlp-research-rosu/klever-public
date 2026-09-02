#!/usr/bin/env python3
"""Mechanical final checks for REVIEW.md structure and evidence links."""

from __future__ import annotations

from pathlib import Path
import re


review = Path("/audit-output/REVIEW.md")
text = review.read_text(encoding="utf-8")
expected_suffix = "VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n"
assert text.endswith(expected_suffix)
assert text.count("\nVERDICT:") == 1
assert text.count("\nLEGITIMACY:") == 1

for stage in range(1, 8):
    assert re.search(rf"^## {stage}\. ", text, flags=re.MULTILINE), stage

links = re.findall(r"\]\(([^)]+)\)", text)
missing: list[str] = []
for link in links:
    if link.startswith(("http://", "https://", "#")):
        continue
    target = (review.parent / link).resolve()
    if not target.exists():
        missing.append(link)
assert not missing, missing

print(f"review-bytes={review.stat().st_size}")
print("stage-headings=1..7")
print(f"local-links={len(links)}")
print("missing-links=0")
print("terminal-markers=exact")
