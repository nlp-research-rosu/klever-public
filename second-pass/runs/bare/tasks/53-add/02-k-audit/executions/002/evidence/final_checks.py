#!/usr/bin/env python3
"""Consistency checks over the completed audit report and decisive logs."""

from pathlib import Path
import re
import sys


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"


def main() -> int:
    review = (ROOT / "REVIEW.md").read_text()
    expected_end = "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
    assert review.endswith(expected_end)
    assert review.count("VERDICT:") == 1
    assert review.count("LEGITIMACY:") == 1
    sections = re.findall(r"(?m)^## ([1-7])\.", review)
    assert sections == list("1234567")

    positive = (EVIDENCE / "positive_claim.log").read_text()
    assert "#Top" in positive and positive.endswith("EXIT_STATUS: 0\n")

    for name in ("body_mutation_dry_run.log", "vacuity_dry_run.log"):
        assert (EVIDENCE / name).read_text().endswith("EXIT_STATUS: 0\n")
    for name in ("body_mutation_proof.log", "vacuity_proof.log"):
        text = (EVIDENCE / name).read_text()
        assert "WarnStuckClaimState" in text
        assert text.endswith("EXIT_STATUS: 1\n")

    required_scripts = [
        "run_and_log.sh",
        "stage1_integrity.py",
        "differential_test.py",
        "check_program_pinning.py",
        "static_inventory.py",
    ]
    for name in required_scripts:
        assert (EVIDENCE / name).is_file()

    print(f"ordered_review_sections={sections}")
    print("positive_claim=#Top exit 0")
    print("body_mutation=dry-run exit 0, proof exit 1 with stuck state")
    print("vacuity_mutation=dry-run exit 0, proof exit 1 with stuck state")
    print("review_terminal_markers=exact")
    print("FINAL_CHECKS_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
