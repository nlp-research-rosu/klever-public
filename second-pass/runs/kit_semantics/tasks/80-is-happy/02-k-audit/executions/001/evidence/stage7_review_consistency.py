#!/usr/bin/env python3
"""Mechanical consistency checks over the completed audit report and evidence."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


root = Path("/audit-output")
review_path = root / "REVIEW.md"
review = review_path.read_text(encoding="utf-8")
lines = review.splitlines()

assert lines[-2:] == ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
assert review.count("VERDICT: ") == 1
assert review.count("LEGITIMACY: ") == 1
assert re.findall(r"^## ([1-7])\.", review, re.MULTILINE) == list("1234567")

references = sorted(set(re.findall(r"`(evidence/[^`\n]+)`", review)))
missing = [relative for relative in references if not (root / relative).is_file()]
assert not missing, missing

inventory = (root / "evidence/stage5_rule_inventory.md").read_text(encoding="utf-8")
assert "- Sentences: 934" in inventory
assert "- `[no-evaluators]` opaque declarations: 22" in inventory
assert "- `[priority]` sentences: 45" in inventory
assert inventory.count("Disposition: `") == 934

for name in ("stage3_kprove_all.log", "stage3_kprove_loop.log"):
    proof = (root / "evidence" / name).read_text(encoding="utf-8")
    assert "\n#Top\n" in proof
    assert proof.rstrip().endswith("EXIT_STATUS: 0")

mutation_build = (
    root / "evidence/stage6_false_mutation_build.log"
).read_text(encoding="utf-8")
mutation_proof = (
    root / "evidence/stage6_false_mutation_kprove.log"
).read_text(encoding="utf-8")
assert mutation_build.rstrip().endswith("EXIT_STATUS: 0")
assert "WarnStuckClaimState" in mutation_proof
assert "IS\n  #Equals\n    .IntSeq" in mutation_proof
assert mutation_proof.rstrip().endswith("EXIT_STATUS: 1")

print(f"review_sha256={hashlib.sha256(review_path.read_bytes()).hexdigest()}")
print(f"evidence_references={len(references)}")
print("all_referenced_evidence_present=true")
print("seven_stages_in_order=true")
print("final_markers_exact=true")
print("proof_and_mutation_statuses_consistent=true")
