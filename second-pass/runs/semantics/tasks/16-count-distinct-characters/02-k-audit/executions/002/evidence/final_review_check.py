#!/usr/bin/env python3
"""Mechanical completion check for the audit report and key evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"


def main() -> int:
    review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
    lines = review.splitlines()
    assert lines[-2:] == ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
    assert sum(line.startswith("## ") and line[3:5] in {
        "1.",
        "2.",
        "3.",
        "4.",
        "5.",
        "6.",
        "7.",
    } for line in lines) == 7

    positive = [
        "stage3-kprove-all.log",
        "stage3-kprove-load.log",
        "stage3-kprove-call.log",
        "stage4-ground-kprove.log",
    ]
    for name in positive:
        text = (EVIDENCE / name).read_text(encoding="utf-8")
        assert "#Top" in text and text.rstrip().endswith("EXIT_STATUS: 0")

    negative = [
        "stage4-body-mutation-kprove.log",
        "stage6-vacuity-kprove.log",
    ]
    for name in negative:
        text = (EVIDENCE / name).read_text(encoding="utf-8")
        assert "WarnStuckClaimState" in text
        assert text.rstrip().endswith("EXIT_STATUS: 1")

    inventory = json.loads(
        (EVIDENCE / "k-inventory-v2.json").read_text(encoding="utf-8")
    )
    classification = json.loads(
        (EVIDENCE / "k-classification-v2.json").read_text(encoding="utf-8")
    )
    assert len(inventory["records"]) == 1094
    assert len(classification["decisions"]) == 1094
    assert classification["counts"]["USED_FIXED_MODEL_MISMATCH"] == 6
    print("FINAL_LINES: PASS")
    print("SEVEN_STAGE_STRUCTURE: PASS")
    print("POSITIVE_AND_NEGATIVE_EVIDENCE: PASS")
    print("INVENTORY_CLASSIFICATION_COVERAGE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
