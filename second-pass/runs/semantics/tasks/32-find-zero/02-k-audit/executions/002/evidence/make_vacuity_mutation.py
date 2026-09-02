#!/usr/bin/env python3
"""Create a fresh false mutation of the first claim's returned value."""

from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")
EVIDENCE = Path("/audit-output/evidence")


def main() -> int:
    original = (WORK / "spec.k").read_text()
    expected = "bisectLow(VS, bracketLow(VS), bracketHigh(VS))"
    replacement = "bisectHigh(VS, bracketLow(VS), bracketHigh(VS))"
    if original.count(expected) != 1:
        raise RuntimeError(
            f"expected exactly one first-claim result occurrence, found {original.count(expected)}"
        )
    mutated = original.replace(expected, replacement, 1)
    mutated = mutated.replace("module SPEC", "module AUDIT-SPEC-VACUITY", 1)
    scratch_path = WORK / "audit-spec-vacuity.k"
    evidence_path = EVIDENCE / "stage6-spec-vacuity.k"
    scratch_path.write_text(mutated)
    evidence_path.write_text(mutated)
    print(f"original result: {expected}")
    print(f"mutated false result: {replacement}")
    print("satisfying witness: VS = vCons(1, vCons(2, .ValSeq))")
    print(
        "under the candidate's assumed validPolynomial predicate, the positive ground "
        "proof returns the distinct bisectLow constructor"
    )
    print(f"scratch mutation: {scratch_path}")
    print(f"preserved mutation: {evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
