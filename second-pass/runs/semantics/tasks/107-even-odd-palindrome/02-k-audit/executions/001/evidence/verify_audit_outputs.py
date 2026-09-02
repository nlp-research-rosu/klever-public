#!/usr/bin/env python3
"""Final consistency checks for the reviewer-authored audit package."""

from __future__ import annotations

import re
from pathlib import Path


root = Path("/audit-output")
evidence = root / "evidence"
review = (root / "REVIEW.md").read_text()

assert review.endswith("VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n")

referenced = sorted(set(re.findall(r"`(evidence/[^`\s,)]+)", review)))
missing = [relative for relative in referenced if not (root / relative).exists()]
assert not missing, f"missing REVIEW evidence references: {missing}"

for index in range(1, 5):
    log = (evidence / f"stage3-kprove-claim-{index}.log").read_text()
    status = (evidence / f"stage3-kprove-claim-{index}.status").read_text().strip()
    assert status == "0"
    assert re.search(r"^#Top$", log, flags=re.MULTILINE)

assert (evidence / "stage3-kprove-full-spec.status").read_text().strip() == "0"
assert re.search(
    r"^#Top$",
    (evidence / "stage3-kprove-full-spec.log").read_text(),
    flags=re.MULTILINE,
)
assert (evidence / "stage6-vacuity-dry-run.status").read_text().strip() == "0"
assert (evidence / "stage6-vacuity-proof.status").read_text().strip() == "1"
mutation_log = (evidence / "stage6-vacuity-proof.log").read_text()
assert "WarnStuckClaimState" in mutation_log
assert "implication check between the conditions has failed" in mutation_log
assert (evidence / "regenerated-solution.kore").read_bytes() == (
    evidence / "verification-expanded.kore"
).read_bytes()

print(f"review_evidence_references={len(referenced)}")
print("missing_references=0")
print("positive_claims_top=4")
print("full_spec_top=true")
print("mutation_builds=true mutation_rejected=true")
print("program_kore_identity=true")
print("review_terminal_markers=true")
