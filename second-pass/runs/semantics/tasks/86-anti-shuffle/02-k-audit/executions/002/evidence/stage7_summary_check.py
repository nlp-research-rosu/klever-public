#!/usr/bin/env python3
"""Final consistency checks over the reviewer-authored report and decisive logs."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"


def require(path: Path, needles: tuple[str, ...]) -> int:
    text = path.read_text(encoding="utf-8")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        print(f"ERROR {path.name} missing={missing}")
        return 1
    print(f"OK {path.name} contains={needles}")
    return 0


def main() -> int:
    failures = 0
    report = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
    lines = report.splitlines()
    expected_tail = ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
    if lines[-2:] != expected_tail:
        print(f"ERROR report tail={lines[-2:]!r}")
        failures += 1
    else:
        print(f"OK report tail={expected_tail!r}")
    if report.count("VERDICT:") != 1 or report.count("LEGITIMACY:") != 1:
        print("ERROR verdict marker counts are not exactly one each")
        failures += 1
    else:
        print("OK verdict marker counts are exactly one each")

    for name in (
        "stage3-kprove-word.log",
        "stage3-kprove-loop.log",
        "stage3-kprove-full.log",
        "stage4-ground-proof.log",
        "stage4-kprove-body-mutation.log",
        "stage5-split-fixed.log",
        "stage5-split-extended.log",
        "stage5-word-fixed.log",
        "stage5-word-extended.log",
        "stage5-loop-fixed.log",
        "stage5-loop-extended.log",
    ):
        failures += require(EVIDENCE / name, ("#Top", "EXIT_STATUS: 0"))

    failures += require(
        EVIDENCE / "stage4-body-mutation-pinning.log",
        (
            "FUNCTION_BODY_TOKEN_EQUAL=True",
            "LOOP_BODY_TOKEN_EQUAL=True",
            "PINNING_FAILURES=0",
            "EXIT_STATUS: 0",
        ),
    )
    failures += require(
        EVIDENCE / "stage6-false-dry-run.log",
        ("kore-exec", "EXIT_STATUS: 0"),
    )
    failures += require(
        EVIDENCE / "stage6-false-kprove.log",
        ("WarnStuckClaimState", "EXIT_STATUS: 1"),
    )
    failures += require(
        EVIDENCE / "stage1-integrity.log",
        ("INTEGRITY_FAILURES=0", "EXIT_STATUS: 0"),
    )
    failures += require(
        EVIDENCE / "stage2-differential.log",
        ("TOTAL_CASES=38475", "MISMATCHES=0", "EXIT_STATUS: 0"),
    )
    print(f"SUMMARY_FAILURES={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
