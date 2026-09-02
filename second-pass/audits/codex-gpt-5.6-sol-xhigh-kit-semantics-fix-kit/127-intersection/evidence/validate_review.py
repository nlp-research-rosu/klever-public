#!/usr/bin/env python3
"""Final structural validation of REVIEW.md and its cited local evidence."""

from __future__ import annotations

import re
from pathlib import Path


review = Path("/audit-output/REVIEW.md")
text = review.read_text()
lines = text.splitlines()

expected_markers = ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]
assert lines[-2:] == expected_markers, lines[-2:]
assert text.endswith("LEGITIMACY: LEGIT\n")

headings = re.findall(r"^## ([1-7])\.", text, flags=re.MULTILINE)
assert headings == list("1234567"), headings

links = re.findall(r"\]\((evidence/[^)]+)\)", text)
missing = sorted({link for link in links if not (review.parent / link).is_file()})
assert not missing, missing

print(f"final_markers={expected_markers}")
print(f"ordered_stage_headings={headings}")
print(f"evidence_links={len(links)} unique_evidence_links={len(set(links))}")
print("missing_evidence_links=0")
print("review_validation=passed")
