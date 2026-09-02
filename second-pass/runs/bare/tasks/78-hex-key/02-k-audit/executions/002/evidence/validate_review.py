#!/usr/bin/env python3
"""Mechanical final-shape and evidence-reference checks for REVIEW.md."""

from __future__ import annotations

import re
from pathlib import Path


review_path = Path("/audit-output/REVIEW.md")
text = review_path.read_text()
lines = text.splitlines()

assert lines[-2:] == ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
assert text.count("VERDICT:") == 1
assert text.count("LEGITIMACY:") == 1

for stage in range(1, 8):
    assert re.search(rf"^## {stage}\. ", text, re.MULTILINE), (
        f"missing stage {stage}"
    )

references = sorted(set(re.findall(r"`(evidence/[^`]+)`", text)))
for relative in references:
    path = Path("/audit-output") / relative
    assert path.exists(), f"missing evidence reference: {relative}"

print("stage_headings=7")
print(f"evidence_references={len(references)}")
print("final_markers=PASS/LEGIT")
print("REVIEW_VALIDATION_PASS")
