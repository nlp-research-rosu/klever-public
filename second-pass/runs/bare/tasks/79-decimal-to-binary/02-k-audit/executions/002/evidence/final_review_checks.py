#!/usr/bin/env python3
"""Consistency checks for the completed REVIEW.md and cited evidence."""

from __future__ import annotations

import re
import stat
from pathlib import Path


review_path = Path("/audit-output/REVIEW.md")
review = review_path.read_text()
lines = review.splitlines()
failures = 0


def check(label: str, value: bool) -> None:
    global failures
    print(f"{'PASS' if value else 'FAIL'} {label}")
    failures += not value


print("COMMAND: python3 /audit-output/evidence/final_review_checks.py")
check("exact terminal verdict lines",
      lines[-2:] == ["VERDICT: PASS", "LEGITIMACY: LEGIT"])
check("one VERDICT marker", len(re.findall(r"^VERDICT:", review, re.MULTILINE)) == 1)
check("one LEGITIMACY marker",
      len(re.findall(r"^LEGITIMACY:", review, re.MULTILINE)) == 1)
check("all seven numbered stages present",
      all(f"## {number}." in review for number in range(1, 8)))

links = re.findall(r"\]\((evidence/[^)]+)\)", review)
missing = []
linked_symlinks = []
for relative in links:
    path = Path("/audit-output") / relative
    try:
        mode = path.lstat().st_mode
    except OSError:
        missing.append(relative)
        continue
    if stat.S_ISLNK(mode):
        linked_symlinks.append(relative)
check("all cited evidence files exist", not missing)
check("no cited evidence file is a symlink", not linked_symlinks)
print(f"CITED_EVIDENCE_COUNT={len(links)}")
print(f"MISSING={missing}")
print(f"SYMLINKS={linked_symlinks}")

proof_log = Path("/audit-output/evidence/stage3_rebuild_final.log").read_text()
check("six #Top results in final clean replay", proof_log.count("#Top") == 6)
check("final clean replay driver exit zero", "DRIVER_EXIT_STATUS=0" in proof_log)
check("final concrete replay has zero mismatches",
      "CONCRETE_MISMATCH_COUNT=0" in proof_log)
check("fresh postcondition mutation rejected",
      "EXPECTED_FAILURE_CONFIRMED" in
      Path("/audit-output/evidence/stage6_nonvacuity.log").read_text())
check("body mutation rejected",
      "EXPECTED_FAILURE_CONFIRMED" in
      Path("/audit-output/evidence/stage4_pinning_and_body.log").read_text())
check("provenance checker exited zero",
      "DRIVER_EXIT_STATUS=0" in
      Path("/audit-output/evidence/stage1_integrity.log").read_text())
check("fidelity checker exited zero",
      "DRIVER_EXIT_STATUS=0" in
      Path("/audit-output/evidence/stage2_fidelity.log").read_text())

print(f"SUMMARY failures={failures}")
print(f"EXIT_STATUS={1 if failures else 0}")
raise SystemExit(1 if failures else 0)
