#!/usr/bin/env python3
"""Ground witnesses for every claim family and claimed-result substitution."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid(coefficients):
    return (
        len(coefficients) >= 2
        and len(coefficients) % 2 == 0
        and coefficients[-1] != 0
    )


def poly_acc(coefficients, x, accumulator=0.0, power=1.0):
    for coefficient in coefficients:
        accumulator = accumulator + coefficient * power
        power = power * x
    return accumulator


def claimed_solve_from(coefficients, begin, end):
    while poly_acc(coefficients, begin) * poly_acc(coefficients, end) > 0.0:
        begin = begin * 2.0
        end = end * 2.0
    while end - begin > 1e-10:
        center = (begin + end) / 2.0
        if poly_acc(coefficients, center) * poly_acc(coefficients, begin) > 0.0:
            begin = center
        else:
            end = center
    return begin


def main() -> int:
    root = Path("/tmp/audit-work/32-find-zero")
    canonical = load("witness_canonical", root / "trusted_canonical.py")
    candidate = load("witness_candidate", root / "solution.py")

    claim_witnesses = {
        "poly-loop-empty": {
            "NS": ".NumSeq",
            "L": 1,
            "BASE_keys": [0],
            "requires_not_L_in_keys_BASE": True,
        },
        "poly-loop-int": {
            "NS": "nInt(1, .NumSeq)",
            "L": 1,
            "BASE_keys": [0],
            "requires_not_L_in_keys_BASE": True,
        },
        "poly-loop-float": {
            "NS": "nFloat(1.0, .NumSeq)",
            "L": 1,
            "BASE_keys": [0],
            "requires_not_L_in_keys_BASE": True,
        },
        "expand-loop": {"NS": "nInt(1, nInt(2, .NumSeq))", "validCoeffs": True},
        "bisect-head": {"requires": "none", "ENV": 0, "exit-code": 0},
        "bisect-loop": {"NS": "nInt(1, nInt(2, .NumSeq))", "validCoeffs": True},
        "find-load": {"NS": "nInt(1, nInt(2, .NumSeq))", "validCoeffs": True},
        "find-init": {"NS": "nInt(1, nInt(2, .NumSeq))", "validCoeffs": True},
    }
    print("CLAIM_WITNESSES " + json.dumps(claim_witnesses, sort_keys=True))

    cases = ([1, 2], [-6, 11, -6, 1], [10, 0, 0, 1])
    mismatches = 0
    for coefficients in cases:
        assert valid(coefficients)
        begin = len(coefficients) / -len(coefficients)
        end = len(coefficients) / len(coefficients)
        summary = claimed_solve_from(coefficients, begin, end)
        candidate_result = candidate.find_zero(list(coefficients))
        canonical_result = canonical.find_zero(list(coefficients))
        record = {
            "coefficients": coefficients,
            "initial_B0": begin,
            "initial_E0": end,
            "validCoeffs": valid(coefficients),
            "claimed_solveFrom": summary,
            "candidate_python": candidate_result,
            "canonical_python": canonical_result,
            "summary_equals_candidate": summary == candidate_result,
            "candidate_close_to_canonical_1e-8": abs(candidate_result - canonical_result) <= 1e-8,
        }
        if not record["summary_equals_candidate"] or not record["candidate_close_to_canonical_1e-8"]:
            mismatches += 1
        print(json.dumps(record, sort_keys=True))

    print(json.dumps({"mismatches": mismatches, "substitutions": len(cases)}, sort_keys=True))
    return mismatches


if __name__ == "__main__":
    raise SystemExit(main())
