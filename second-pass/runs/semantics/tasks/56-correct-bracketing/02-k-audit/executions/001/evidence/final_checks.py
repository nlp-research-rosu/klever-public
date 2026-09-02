#!/usr/bin/env python3
"""Consistency checks for the completed audit package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"


def require_contains(name: str, *needles: str) -> None:
    text = (EVIDENCE / name).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise AssertionError(f"{name} lacks {needle!r}")


def main() -> int:
    review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
    lines = review.splitlines()
    assert lines[-2:] == [
        "VERDICT: CONCERNS",
        "LEGITIMACY: LEGIT",
    ]
    positions = [
        review.index(f"## Stage {stage} ")
        for stage in range(1, 8)
    ]
    assert positions == sorted(positions)

    require_contains("10-prove-all-positive.log", "#Top", "EXIT_STATUS: 0")
    require_contains("22-prove-loop-claim-pair.log", "#Top", "EXIT_STATUS: 0")
    require_contains(
        "21-false-postcondition.log",
        "WarnStuckClaimState",
        "notBool bracketResult",
        "EXIT_STATUS: 1",
    )
    require_contains(
        "20-body-mutation.log",
        "WarnStuckClaimState",
        "false ~> .K",
        "EXIT_STATUS: 1",
    )
    require_contains(
        "14-prove-fixed-expression-bridges.log",
        "#Top",
        "EXIT_STATUS: 0",
    )
    require_contains("16-prove-fixed-pop-ground.log", "#Top", "EXIT_STATUS: 0")

    with (EVIDENCE / "rule-inventory.tsv").open(
        encoding="utf-8", newline=""
    ) as stream:
        row_count = sum(1 for _ in csv.DictReader(stream, dialect="excel-tab"))
    assert row_count == 949

    symlinks = [str(path) for path in EVIDENCE.iterdir() if path.is_symlink()]
    assert not symlinks
    digest = hashlib.sha256(review.encode("utf-8")).hexdigest()
    print(f"review_sha256={digest}")
    print(f"inventory_rows={row_count}")
    print(f"evidence_file_count={sum(1 for path in EVIDENCE.iterdir() if path.is_file())}")
    print("final_markers_exact=true")
    print("stage_order_exact=true")
    print("expected_positive_and_negative_signals_present=true")
    print("evidence_symlink_count=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
