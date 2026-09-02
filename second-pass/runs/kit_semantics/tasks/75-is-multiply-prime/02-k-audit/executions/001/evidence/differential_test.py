#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 75."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_multiply_prime


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: differential_test.py CANONICAL_PY SOLUTION_PY")

    canonical = load_function("trusted_canonical", Path(sys.argv[1]))
    generated = load_function("candidate_solution", Path(sys.argv[2]))

    # 0..99 exhausts the nonnegative intended domain. Extra negative cases
    # exercise the contract's unbounded-below A < 100 portion, including
    # deterministic generated values and large-magnitude boundaries.
    rng = random.Random(750075)
    inputs = set(range(0, 100))
    inputs.update({-1, -2, -3, -7, -8, -99, -100, -101, -10**6, -(10**30)})
    inputs.update(-rng.randrange(1, 10**12) for _ in range(24))

    # Explicitly assert that every disjunction branch and both adjacent
    # boundaries are represented by the exhaustive 0..99 block.
    true_branches = {
        8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50,
        52, 63, 66, 68, 70, 75, 76, 78, 92, 98, 99,
    }
    branch_boundaries = {
        x for value in true_branches for x in (value - 1, value, value + 1)
        if x < 100
    }
    assert true_branches <= inputs
    assert branch_boundaries <= inputs
    assert 30 in inputs  # documented example

    mismatches: list[dict[str, object]] = []
    records: list[dict[str, object]] = []
    for value in sorted(inputs):
        expected = canonical(value)
        actual = generated(value)
        record = {
            "input": value,
            "canonical": expected,
            "generated": actual,
            "canonical_type": type(expected).__name__,
            "generated_type": type(actual).__name__,
        }
        records.append(record)
        if expected is not actual:
            mismatches.append(record)

    print(json.dumps({
        "oracle": str(Path(sys.argv[1]).resolve()),
        "candidate": str(Path(sys.argv[2]).resolve()),
        "documented_example": 30,
        "input_count": len(records),
        "inputs": [r["input"] for r in records],
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "true_inputs": [r["input"] for r in records if r["canonical"] is True],
    }, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
