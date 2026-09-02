#!/usr/bin/env python3
"""Mechanical completion checks for REVIEW.md and decisive evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"
review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
lines = review.splitlines()

assert lines[-2:] == ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
assert review.count("VERDICT: ") == 1
assert review.count("LEGITIMACY: ") == 1

headings = re.findall(r"^## ([1-7])\. ", review, flags=re.MULTILINE)
assert headings == ["1", "2", "3", "4", "5", "6", "7"], headings

for target in re.findall(r"\]\((evidence/[^)]+)\)", review):
    assert (ROOT / target).is_file(), target

integrity = (EVIDENCE / "01-integrity.log").read_text(encoding="utf-8")
assert "semantics diff status: 0" in integrity
assert "prompt cmp status: 0" in integrity
assert "translator cmp status: 0" in integrity

translation = (EVIDENCE / "02_regenerate_solution.log").read_text(encoding="utf-8")
assert "byte-identity cmp status: 0" in translation
assert translation.rstrip().endswith("EXIT STATUS: 0")

differential = (EVIDENCE / "02_differential.log").read_text(encoding="utf-8")
assert "input count: 1034" in differential
assert "candidate/exact-decimal mismatch count: 2" in differential
assert differential.rstrip().endswith("EXIT STATUS: 1")

positive = (EVIDENCE / "03_kprove_spec.log").read_text(encoding="utf-8")
assert "#Top" in positive
assert positive.rstrip().endswith("EXIT STATUS: 0")

pinning = (EVIDENCE / "04_pinning_test.log").read_text(encoding="utf-8")
assert "#Top" in pinning
assert re.search(r"\n777\n", pinning)
assert pinning.rstrip().endswith("EXIT STATUS: 0")

false_dry = (EVIDENCE / "06_false_dry_run.log").read_text(encoding="utf-8")
false_proof = (EVIDENCE / "06_false_kprove.log").read_text(encoding="utf-8")
assert false_dry.rstrip().endswith("EXIT STATUS: 0")
assert "WarnStuckClaimState" in false_proof
assert false_proof.rstrip().endswith("EXIT STATUS: 1")

inventory = json.loads((EVIDENCE / "05_rule_inventory.json").read_text(encoding="utf-8"))
assert len(inventory) == 1102
assert sum(record["kind"] == "rule" for record in inventory) == 698
assert sum(record["kind"] == "syntax" for record in inventory) == 230

print("review markers: exact")
print("seven ordered stages: exact")
print("review evidence links: all present")
print("decisive command statuses and outputs: verified")
print("inventory counts: verified")
