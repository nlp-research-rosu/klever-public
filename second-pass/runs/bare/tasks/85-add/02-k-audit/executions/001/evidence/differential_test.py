#!/usr/bin/env python3
"""Independent differential test for HumanEval 85-add.

The canonical and candidate entry points are loaded from paths supplied on the
command line.  The expected value is computed by an independently written loop,
not by either implementation or by the K summary equations.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_add(module_name: str, path: Path) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


def oracle(values: list[int]) -> int:
    total = 0
    for index in range(1, len(values), 2):
        value = values[index]
        if value % 2 == 0:
            total += value
    return total


def outcome(function: Callable[[list[int]], int], values: list[int]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(values.copy())}
    except BaseException as error:  # Record real outcome differences, including recursion limits.
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py TRUSTED_CANONICAL CANDIDATE", file=sys.stderr)
        return 64

    canonical = load_add("trusted_canonical_85", Path(sys.argv[1]).resolve())
    candidate = load_add("candidate_solution_85", Path(sys.argv[2]).resolve())

    cases: list[tuple[str, list[int]]] = [
        ("documented-example", [4, 2, 6, 7]),
        ("empty-outside-stated-domain", []),
        ("singleton-boundary", [1]),
        ("length-two-even", [9, 8]),
        ("length-two-odd", [9, 7]),
        ("length-two-negative-even", [9, -8]),
        ("length-two-zero", [9, 0]),
        ("length-three", [2, 4, 6]),
        ("multiple-even-odd-indices", [2, 3, 4, 6, 8, 10]),
        ("negative-mix", [-1, -2, -3, -4, -5]),
        ("large-integers", [10**100, -(10**100), -(10**100) + 1, 10**100 + 2]),
        ("long-1998", list(range(1998))),
        ("long-2000", list(range(2000))),
    ]

    alphabet = (-2, -1, 0, 1, 2)
    for length in range(0, 6):
        for values in itertools.product(alphabet, repeat=length):
            cases.append((f"exhaustive-len-{length}", list(values)))

    rng = random.Random(850023)
    for sample in range(3000):
        length = rng.randrange(0, 81)
        values = [rng.randint(-10**12, 10**12) for _ in range(length)]
        cases.append((f"random-{sample}", values))

    mismatches: list[dict[str, Any]] = []
    normal_value_mismatches = 0
    outcome_mismatches = 0
    for label, values in cases:
        expected = {"kind": "return", "value": oracle(values)}
        canonical_outcome = outcome(canonical, values)
        candidate_outcome = outcome(candidate, values)
        if canonical_outcome != expected or candidate_outcome != expected:
            mismatch = {
                "label": label,
                "length": len(values),
                "values_head": values[:12],
                "oracle": expected,
                "canonical": canonical_outcome,
                "candidate": candidate_outcome,
            }
            mismatches.append(mismatch)
            if candidate_outcome["kind"] == "return" and candidate_outcome != expected:
                normal_value_mismatches += 1
            if candidate_outcome["kind"] != expected["kind"]:
                outcome_mismatches += 1

    report = {
        "case_count": len(cases),
        "documented_cases": 13,
        "exhaustive_scope": "all lists of lengths 0..5 over [-2,-1,0,1,2]",
        "random_scope": "3000 lists, lengths 0..80, fixed seed 850023, values in [-10^12,10^12]",
        "long_scope": "lengths 1998 and 2000 to exercise the real interpreter recursion boundary",
        "mismatch_count": len(mismatches),
        "normal_value_mismatch_count": normal_value_mismatches,
        "outcome_mismatch_count": outcome_mismatches,
        "mismatches": mismatches,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
