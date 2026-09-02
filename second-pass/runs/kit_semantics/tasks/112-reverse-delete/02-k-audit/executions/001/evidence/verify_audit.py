#!/usr/bin/env python3
"""Final self-check for review markers, evidence presence, and log outcomes."""

from __future__ import annotations

import csv
import pathlib
import re
import sys


ROOT = pathlib.Path("/audit-output")
EVIDENCE = ROOT / "evidence"

REQUIRED = [
    "00-toolchain.log",
    "01-integrity.log",
    "01-generation-records.log",
    "02-translation-identity.log",
    "02-differential.log",
    "03-kompile-concrete.log",
    "03-concrete-execution.log",
    "03-kompile-proof.log",
    "03-kprove-all.log",
    "03-kprove-loop.log",
    "03-kprove-entry-with-loop-helper.log",
    "04-program-pinning.log",
    "04-claim-witness.log",
    "04-body-mutant-build.log",
    "04-body-mutant-proof.log",
    "05-rule-inventory.log",
    "06-false-result-build.log",
    "06-false-result-proof.log",
    "auditor-body-mutant.k",
    "auditor-false-result.k",
    "concrete_cases.py",
    "construct-map.md",
    "rule-inventory.tsv",
]

EXPECTED_STATUS = {
    "02-translation-identity.log": 0,
    "02-differential.log": 0,
    "03-kompile-concrete.log": 0,
    "03-concrete-execution.log": 0,
    "03-kompile-proof.log": 0,
    "03-kprove-all.log": 0,
    "03-kprove-loop.log": 0,
    "03-kprove-entry-with-loop-helper.log": 0,
    "04-program-pinning.log": 0,
    "04-claim-witness.log": 0,
    "04-body-mutant-build.log": 0,
    "04-body-mutant-proof.log": 1,
    "05-rule-inventory.log": 0,
    "06-false-result-build.log": 0,
    "06-false-result-proof.log": 1,
}


def main() -> int:
    failures: list[str] = []
    for name in REQUIRED:
        path = EVIDENCE / name
        if not path.is_file() or path.is_symlink():
            failures.append(f"missing/non-regular evidence: {path}")

    for name, expected in EXPECTED_STATUS.items():
        text = (EVIDENCE / name).read_text(encoding="utf-8")
        match = re.search(r"^EXIT_STATUS: (-?\d+)$", text, re.MULTILINE)
        actual = int(match.group(1)) if match else None
        if actual != expected:
            failures.append(f"{name}: expected logged exit {expected}, got {actual}")

    for name in [
        "03-kprove-all.log",
        "03-kprove-loop.log",
        "03-kprove-entry-with-loop-helper.log",
    ]:
        if "\n#Top\n" not in (EVIDENCE / name).read_text(encoding="utf-8"):
            failures.append(f"{name}: missing #Top")

    for name in ["04-body-mutant-proof.log", "06-false-result-proof.log"]:
        text = (EVIDENCE / name).read_text(encoding="utf-8")
        if "WarnStuckClaimState" not in text or "[Error] Prover" not in text:
            failures.append(f"{name}: missing expected stuck-claim diagnostics")

    rows = list(
        csv.DictReader(
            (EVIDENCE / "rule-inventory.tsv").open(encoding="utf-8"),
            delimiter="\t",
        )
    )
    rule_count = sum(row["kind"] == "rule" for row in rows)
    syntax_count = sum(row["kind"] == "syntax" for row in rows)
    if (rule_count, syntax_count) != (699, 229):
        failures.append(
            f"inventory count mismatch: rules={rule_count}, syntax={syntax_count}"
        )
    if any(not row["decision"] for row in rows):
        failures.append("inventory contains row without decision")

    review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
    if not review.endswith("VERDICT: PASS\nLEGITIMACY: LEGIT\n"):
        failures.append("REVIEW.md does not end with exact expected markers")
    if review.count("\nVERDICT:") != 1 or review.count("\nLEGITIMACY:") != 1:
        failures.append("REVIEW.md contains extra verdict markers")

    print(f"required_evidence_files={len(REQUIRED)}")
    print(f"checked_log_statuses={len(EXPECTED_STATUS)}")
    print(f"inventory_rows={len(rows)} rules={rule_count} syntax={syntax_count}")
    print(f"review_bytes={len(review.encode())}")
    if failures:
        for failure in failures:
            print(f"FAILURE: {failure}")
        return 1
    print("RESULT: evidence and final markers are complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
