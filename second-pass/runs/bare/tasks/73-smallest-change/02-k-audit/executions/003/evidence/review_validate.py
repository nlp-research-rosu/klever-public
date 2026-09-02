#!/usr/bin/env python3
"""Mechanical final-format and evidence-reference check for REVIEW.md."""

from __future__ import annotations

import re
from pathlib import Path


review = Path("/audit-output/REVIEW.md").read_text()
expected_suffix = "VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n"
headings = re.findall(r"^## ([1-7])\. ", review, flags=re.MULTILINE)
evidence_links = re.findall(r"\]\((/audit-output/evidence/[^)]+)\)", review)
missing = [path for path in evidence_links if not Path(path).exists()]
print(f"seven_stage_headings={headings}")
print(f"stage_headings_exact={headings == list('1234567')}")
print(f"verdict_suffix_exact={review.endswith(expected_suffix)}")
print(f"verdict_marker_count={review.count('VERDICT:')}")
print(f"legitimacy_marker_count={review.count('LEGITIMACY:')}")
print(f"evidence_link_count={len(evidence_links)}")
print(f"missing_evidence_links={missing}")
ok = (
    headings == list("1234567")
    and review.endswith(expected_suffix)
    and review.count("VERDICT:") == 1
    and review.count("LEGITIMACY:") == 1
    and not missing
)
raise SystemExit(0 if ok else 1)
