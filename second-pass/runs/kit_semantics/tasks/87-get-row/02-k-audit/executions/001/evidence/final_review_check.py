#!/usr/bin/env python3
"""Mechanical completeness checks for REVIEW.md and decisive evidence."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/audit-output")
REVIEW = ROOT / "REVIEW.md"


def require_text(path: Path, *needles: str) -> None:
    text = path.read_text()
    for needle in needles:
        assert needle in text, f"{needle!r} missing from {path}"


def main() -> None:
    review = REVIEW.read_text()
    lines = review.splitlines()
    assert lines[-2:] == ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"]
    assert review.count("VERDICT:") == 1
    assert review.count("LEGITIMACY:") == 1

    references = re.findall(r"\]\((evidence/[^)]+)\)", review)
    missing = [relative for relative in references if not (ROOT / relative).is_file()]
    assert not missing, f"missing cited evidence: {missing}"

    for name in (
        "stage3-kprove-shape.log",
        "stage3-kprove-spec.log",
        "stage3-kprove-inner-outer.log",
        "stage3-kprove-column-key.log",
        "stage3-kprove-row-key.log",
        "stage5-shape-context-proof.log",
    ):
        require_text(ROOT / "evidence" / name, "#Top", "EXIT STATUS: 0")

    require_text(
        ROOT / "evidence" / "stage6-mutation-build.log",
        "EXIT STATUS: 0",
    )
    require_text(
        ROOT / "evidence" / "stage6-mutation-proof.log",
        "WarnStuckClaimState",
        "<k>\n    ref ( 2 ) ~> .K",
        "EXIT STATUS: 1",
    )
    require_text(
        ROOT / "evidence" / "stage1-integrity.log",
        "SEMANTICS_TREE_MISMATCH_COUNT: 0",
        "ALL_STAGE1_INTEGRITY_CHECKS_PASSED",
    )
    require_text(
        ROOT / "evidence" / "stage2-differential.log",
        "total_cases=11576",
        "mismatches=0",
        "EXIT STATUS: 0",
    )
    require_text(
        ROOT / "evidence" / "stage4-constructor-pinning.log",
        "ALL_THREE_SUBMITTED_FUNCTION_BODIES_PINNED",
        "EXIT STATUS: 0",
    )
    print(f"cited_evidence_paths={len(references)}")
    print("missing_cited_evidence=0")
    print("positive_proof_signals=present")
    print("fresh_mutation_expected_failure=present")
    print("review_terminal_markers=exact")


if __name__ == "__main__":
    main()
