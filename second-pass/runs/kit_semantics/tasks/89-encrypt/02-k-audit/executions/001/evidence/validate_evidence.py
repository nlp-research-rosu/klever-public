#!/usr/bin/env python3
"""Final consistency checks over reviewer-authored evidence and REVIEW.md."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"


def require(path: str, fragments: list[str]) -> None:
    text = (EVIDENCE / path).read_text(encoding="utf-8")
    for fragment in fragments:
        assert fragment in text, (path, fragment)


def main() -> None:
    require("01-provenance.log", ["PROVENANCE_CHECK=PASS", "EXIT_STATUS: 0"])
    require("02-translator-identity.log", ["TRANSLATOR_BYTE_IDENTITY=PASS", "EXIT_STATUS: 0"])
    require("02-differential.log", ["mismatches=0", "DIFFERENTIAL_CHECK=PASS", "EXIT_STATUS: 0"])
    require("03-concrete-build-run.log", ["<k>", ".K", "NoExc", "EXIT_STATUS: 0"])
    require("03-proof-build.log", ["EXIT_STATUS: 0"])
    require("03-kprove-encrypt-loop.log", ["#Top", "EXIT_STATUS: 0"])
    require("03-kprove-all-claims.log", ["#Top", "EXIT_STATUS: 0"])
    require("04-program-pinning.log", ["PROGRAM_PINNING=PASS", "EXIT_STATUS: 0"])
    require("04-body-sensitivity-proof.log", ["iCons ( 98", "WarnStuckClaimState", "EXIT_STATUS: 1"])
    require("05-rule-inventory-generation.log", ["inventory_items=1030", "EXIT_STATUS: 0"])
    require("05-proof-local-checks.log", ["PROOF_LOCAL_CHECKS=PASS", "EXIT_STATUS: 0"])
    require("06-vacuity-dry-run.log", ["EXIT_STATUS: 0"])
    require("06-vacuity-proof.log", ["iCons ( 100", "WarnStuckClaimState", "EXIT_STATUS: 1"])

    review_lines = (ROOT / "REVIEW.md").read_text(encoding="utf-8").splitlines()
    assert review_lines[-2:] == ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
    assert sum(line.startswith("## ") and line[3:5] in {f"{n}." for n in range(1, 8)} for line in review_lines) == 7
    print("positive_target_logs=#Top_and_exit_0")
    print("fresh_vacuity_log=expected_stuck_exit_1")
    print("body_sensitivity_log=expected_stuck_exit_1")
    print("review_final_markers=PASS_LEGIT")
    print("EVIDENCE_VALIDATION=PASS")


if __name__ == "__main__":
    main()
