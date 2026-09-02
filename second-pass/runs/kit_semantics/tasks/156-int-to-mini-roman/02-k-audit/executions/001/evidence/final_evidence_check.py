#!/usr/bin/env python3
"""Final consistency check for the reviewer-authored report and evidence set."""

from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"PASS: {message}")


def main() -> int:
    output = Path("/audit-output")
    evidence = output / "evidence"
    review = (output / "REVIEW.md").read_text(encoding="utf-8")
    require("PENDING_" not in review, "no pending report placeholders")
    require(
        review.rstrip().endswith("VERDICT: PASS\nLEGITIMACY: LEGIT"),
        "report ends in the exact paired verdict markers",
    )
    require(review.count("VERDICT:") == 1, "one verdict marker")
    require(review.count("LEGITIMACY:") == 1, "one legitimacy marker")

    required = [
        "stage1_integrity.log",
        "trace_inventory.log",
        "translation_identity.log",
        "differential.log",
        "kompile_llvm.log",
        "krun_concrete.log",
        "kompile_haskell.log",
        "pinning_audit.log",
        "static_inventory_summary.log",
        "declaration_inventory.txt",
        "static_rule_review.md",
        "used_constructs.md",
        "positive_log_audit.log",
        "kompile_body_mutant.log",
        "kprove_body_mutant.log",
        "kprove_false_dry_run.log",
        "kprove_false.log",
        "negative_probes_driver.log",
    ]
    for name in required:
        require((evidence / name).is_file(), f"evidence file exists: {name}")
    for batch in range(1, 11):
        require(
            (evidence / f"kprove_positive_{batch:02d}.log").is_file(),
            f"fresh positive batch log {batch:02d} exists",
        )

    positive = (evidence / "positive_log_audit.log").read_text(encoding="utf-8")
    require("coverage=every claim 1..1000 exactly once" in positive,
            "positive coverage is exact")
    require("RESULT=PASS" in positive and positive.rstrip().endswith(
        "EXIT_STATUS: 0"
    ), "positive log audit exits 0")

    body = (evidence / "kprove_body_mutant.log").read_text(encoding="utf-8")
    require("WarnStuckClaimState" in body and body.rstrip().endswith(
        "EXIT_STATUS: 1"
    ), "executed-body mutation has expected stuck residual")
    dry = (evidence / "kprove_false_dry_run.log").read_text(encoding="utf-8")
    require(dry.rstrip().endswith("EXIT_STATUS: 0"),
            "fresh false mutation builds in dry-run")
    false = (evidence / "kprove_false.log").read_text(encoding="utf-8")
    require("WarnStuckClaimState" in false and false.rstrip().endswith(
        "EXIT_STATUS: 1"
    ), "fresh false mutation has expected stuck residual")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
