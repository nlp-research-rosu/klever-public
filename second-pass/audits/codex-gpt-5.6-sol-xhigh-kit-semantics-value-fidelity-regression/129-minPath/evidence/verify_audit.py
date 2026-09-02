#!/usr/bin/env python3
"""Final consistency checks for the reviewer-authored report and evidence."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/audit-output")
REVIEW = ROOT / "REVIEW.md"


def main() -> int:
    text = REVIEW.read_text(encoding="utf-8")
    expected_footer = "VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n"
    assert text.endswith(expected_footer)
    assert text.count("VERDICT:") == 1
    assert text.count("LEGITIMACY:") == 1

    missing = []
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"):
            continue
        resolved = (REVIEW.parent / target).resolve()
        if not resolved.exists():
            missing.append((target, str(resolved)))
    assert not missing, missing

    proof_logs = (
        "18-prove-find-one-loop.log",
        "19-prove-locate-one-loop.log",
        "20-prove-scan-row-loop.log",
        "24-prove-find-neighbor-loop-retry.log",
        "22-prove-result-loop.log",
        "23-prove-minpath-entry.log",
    )
    for name in proof_logs:
        proof = (ROOT / "evidence" / "logs" / name).read_text(encoding="utf-8")
        assert "#Top" in proof, name
        assert proof.endswith("EXIT_STATUS: 0\n"), name

    vacuity = (
        ROOT / "evidence" / "logs" / "26-vacuity-proof-failure.log"
    ).read_text(encoding="utf-8")
    assert "WarnStuckClaimState" in vacuity
    assert vacuity.endswith("EXIT_STATUS: 1\n")

    body_python = (
        ROOT / "evidence" / "logs" / "27-body-witness-python.log"
    ).read_text(encoding="utf-8")
    body_krun = (
        ROOT / "evidence" / "logs" / "29-body-witness-fixed-krun.log"
    ).read_text(encoding="utf-8")
    body_proof = (
        ROOT / "evidence" / "logs" / "31-body-witness-proof.log"
    ).read_text(encoding="utf-8")
    assert "[1, 999, 1]" in body_python
    assert "vCons ( 999" in body_krun
    assert "#Top" in body_proof and body_proof.endswith("EXIT_STATUS: 0\n")

    print("review footer: exact")
    print("review links: all targets exist")
    print("six isolated positive proofs: #Top / exit 0")
    print("fresh vacuity mutation: stuck / exit 1")
    print("body sensitivity witness: fixed result 999 / extended proof #Top")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
