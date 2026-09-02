#!/usr/bin/env python3
"""Sanity-check the completed audit report and its decisive evidence."""

from __future__ import annotations

from pathlib import Path


root = Path("/audit-output")
evidence = root / "evidence"
review = root / "REVIEW.md"

required = {
    "00-environment.log": ("EXIT_STATUS: 0",),
    "01-integrity.log": ("INTEGRITY_FAILURE_COUNT 0", "EXIT_STATUS: 0"),
    "03-translation-fidelity.log": ("EXIT_STATUS: 0",),
    "04-differential.log": ("mismatch_count=0", "EXIT_STATUS: 0"),
    "05-kompile-runtime.log": ("EXIT_STATUS: 0",),
    "07-krun-concrete-tests.log": ("EXIT_STATUS: 0",),
    "08-kompile-verification.log": ("EXIT_STATUS: 0",),
    "10-kprove-spec.log": ("#Top", "EXIT_STATUS: 0"),
    "12-ground-adequacy.log": ("#Top", "EXIT_STATUS: 0"),
    "13-vacuity-dry-run.log": ("EXIT_STATUS: 0",),
    "14-vacuity-proof.log": ("WarnStuckClaimState", "EXIT_STATUS: 1"),
    "15-body-mutant-build.log": ("EXIT_STATUS: 0",),
    "16-body-mutant-proof.log": ("WarnStuckClaimState", "EXIT_STATUS: 1"),
}

failures: list[str] = []
for name, needles in required.items():
    path = evidence / name
    if not path.is_file() or path.stat().st_size == 0:
        failures.append(f"missing-or-empty {path}")
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            failures.append(f"{path}: missing {needle!r}")

review_lines = review.read_text(encoding="utf-8").splitlines()
expected_tail = ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]
if review_lines[-2:] != expected_tail:
    failures.append(f"bad report tail: {review_lines[-2:]!r}")
if sum(line.startswith("VERDICT: ") for line in review_lines) != 1:
    failures.append("report must have exactly one VERDICT marker")
if sum(line.startswith("LEGITIMACY: ") for line in review_lines) != 1:
    failures.append("report must have exactly one LEGITIMACY marker")

print(f"review_lines={len(review_lines)}")
print(f"evidence_files={sum(path.is_file() for path in evidence.iterdir())}")
print(f"failure_count={len(failures)}")
for failure in failures:
    print(f"FAILURE {failure}")
raise SystemExit(1 if failures else 0)
