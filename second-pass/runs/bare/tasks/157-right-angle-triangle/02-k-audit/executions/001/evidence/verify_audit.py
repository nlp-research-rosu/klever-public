#!/usr/bin/env python3
"""Mechanical completion checks for REVIEW.md and its decisive evidence."""

from __future__ import annotations

import pathlib
import re


OUTPUT = pathlib.Path("/audit-output")
EVIDENCE = OUTPUT / "evidence"
REVIEW = OUTPUT / "REVIEW.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def read(name: str) -> str:
    return (EVIDENCE / name).read_text(encoding="utf-8")


def main() -> int:
    review = REVIEW.read_text(encoding="utf-8")
    lines = review.splitlines()
    require(
        lines[-2:] == ["VERDICT: CONCERNS", "LEGITIMACY: LEGIT"],
        "terminal verdict markers are exact",
    )
    require(
        sum(line.startswith("VERDICT:") for line in lines) == 1,
        "exactly one VERDICT marker",
    )
    require(
        sum(line.startswith("LEGITIMACY:") for line in lines) == 1,
        "exactly one LEGITIMACY marker",
    )
    for stage in range(1, 8):
        require(f"## {stage}." in review, f"stage {stage} heading is present")

    absolute_links = re.findall(r"\]\((/[^)]+)\)", review)
    missing = [target for target in absolute_links if not pathlib.Path(target).exists()]
    require(not missing, f"all {len(absolute_links)} absolute evidence links exist")

    for name in (
        "stage3-kompile-semantic.log",
        "stage3-kompile-verification.log",
        "stage3-kprove-all-claims.log",
        "stage3-kprove-claim-1.log",
        "stage3-kprove-claim-2.log",
        "stage3-kprove-claim-3.log",
        "stage3-kprove-claim-4.log",
        "stage3-concrete-comparison.log",
        "stage4-program-final-diff.log",
        "stage6-vacuity-dry-run.log",
    ):
        require("exit_status: 0" in read(name), f"{name} records exit 0")

    for name in (
        "stage3-kprove-all-claims.log",
        "stage3-kprove-claim-1.log",
        "stage3-kprove-claim-2.log",
        "stage3-kprove-claim-3.log",
        "stage3-kprove-claim-4.log",
    ):
        require("#Top" in read(name), f"{name} records #Top")

    translation = read("stage2-translation.log")
    require(
        translation.count(
            "d5ca368d0cd54dd51a7a7b8ea8a62b4ce92b31978b8484435101265b40c7301a"
        )
        == 2,
        "translation log records matching regenerated/submitted hashes",
    )

    concrete = read("stage3-concrete-comparison.log")
    require(
        '"k_candidate_mismatches": 0' in concrete,
        "fresh concrete K/Python comparison has zero mismatches",
    )

    mutation = read("stage6-vacuity-proof.log")
    require("exit_status: 1" in mutation, "false mutation records exit 1")
    require("WarnStuckClaimState" in mutation, "false mutation is a stuck claim")
    require("result ( true )" in mutation, "false mutation residual exposes true result")

    require(
        read("stage1-integrity.log").rstrip().endswith("exit_status: 0"),
        "integrity command completed successfully",
    )
    print("ALL_AUDIT_CHECKS_PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
