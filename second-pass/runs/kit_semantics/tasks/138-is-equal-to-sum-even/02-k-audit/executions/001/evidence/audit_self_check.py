#!/usr/bin/env python3
"""Final structural and evidence sanity checks for the reviewer output."""

from __future__ import annotations

import re
from pathlib import Path


review_path = Path("/audit-output/REVIEW.md")
review = review_path.read_text()
expected_tail = "VERDICT: PASS\nLEGITIMACY: LEGIT"
assert review.rstrip().endswith(expected_tail)
assert review.count("VERDICT:") == 1
assert review.count("LEGITIMACY:") == 1

positions = []
for stage in range(1, 8):
    match = re.search(rf"^## {stage}\. ", review, re.MULTILINE)
    assert match is not None, f"missing stage {stage}"
    positions.append(match.start())
assert positions == sorted(positions)

for target in re.findall(r"\]\((/audit-output/evidence/[^)]+)\)", review):
    assert Path(target).is_file(), f"missing evidence link: {target}"

positive = Path("/audit-output/evidence/05-positive-kprove.log").read_text()
false_mutation = Path("/audit-output/evidence/10-false-mutation.log").read_text()
body_mutation = Path("/audit-output/evidence/11-body-sensitivity.log").read_text()
assert "#Top" in positive and "EXIT_STATUS=0" in positive
assert "DRY_RUN_EXIT=0" in false_mutation
assert "WarnStuckClaimState" in false_mutation
assert "MUTATION_PROOF_EXIT=1" in false_mutation
assert "<k>\n    true ~> .K" in false_mutation
assert "DRY_RUN_EXIT=0" in body_mutation
assert "WarnStuckClaimState" in body_mutation
assert "BODY_MUTATION_PROOF_EXIT=1" in body_mutation
assert "<k>\n    false ~> .K" in body_mutation

evidence_link_count = len(re.findall(r"\]\(/audit-output/evidence/", review))
print(f"review_bytes={review_path.stat().st_size}")
print(f"evidence_links={evidence_link_count}")
print("seven_stages_in_order=true")
print("terminal_markers_exact=true")
print("positive_and_negative_evidence_signals=true")
print("AUDIT_SELF_CHECK=PASS")
