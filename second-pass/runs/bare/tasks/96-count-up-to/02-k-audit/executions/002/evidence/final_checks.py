#!/usr/bin/env python3
"""Mechanical publication checks for the completed adversarial audit."""

from pathlib import Path


output = Path("/audit-output")
evidence = output / "evidence"
review = (output / "REVIEW.md").read_text(encoding="utf-8")
lines = review.splitlines()
assert lines[-2:] == ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]
assert review.endswith("VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n")
for stage in range(1, 8):
    assert f"## {stage}." in review

positive_logs = [
    "03-kprove-trial.log",
    "03-kprove-scan.log",
    "03-kprove-entry.log",
]
for name in positive_logs:
    text = (evidence / name).read_text(encoding="utf-8")
    assert "\n#Top\n" in text
    assert text.endswith("EXIT_STATUS: 0\n")

dry_run = (evidence / "06-vacuity-dry-run.log").read_text(encoding="utf-8")
assert dry_run.endswith("EXIT_STATUS: 0\n")
mutation = (evidence / "06-vacuity-proof.log").read_text(encoding="utf-8")
assert "WarnStuckClaimState" in mutation
assert "implication check between the conditions has failed" in mutation
assert mutation.endswith("EXIT_STATUS: 1\n")

required = [
    "01-integrity.log",
    "01-trace-summary.log",
    "02-translation.log",
    "02-differential.log",
    "03-kompile-semantics.log",
    "03-kompile-verification.log",
    "03-concrete-compare.log",
    "04-program-pinning.log",
    "04-body-mutation-kprove.log",
    "04-satisfying-witnesses.txt",
    "05-rule-inventory.md",
    "06-spec-vacuity-audit.k",
    "07-trust-ledger.md",
]
for name in required:
    path = evidence / name
    assert path.is_file() and not path.is_symlink(), name

for path in output.rglob("*"):
    assert not path.is_symlink(), path

print("FINAL_REVIEW_MARKERS_OK")
print("SEVEN_STAGE_STRUCTURE_OK")
print("POSITIVE_PROOF_LOGS_OK count=3")
print("FALSE_MUTATION_LOG_OK")
print(f"EVIDENCE_FILES_OK count={sum(1 for p in evidence.iterdir() if p.is_file())}")
