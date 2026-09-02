#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


def intended_oracle(values: list[int]) -> list[int]:
    """Prompt prose: non-negative integers, ordered by popcount then value."""
    if any(value < 0 for value in values):
        raise ValueError("outside intended non-negative domain")
    return sorted(values, key=lambda value: (value.bit_count(), value))


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py TRUSTED_CANONICAL.py CANDIDATE.py")
        return 64

    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical_116")
    candidate = load_entry(Path(sys.argv[2]), "candidate_solution_116")

    documented = [
        {
            "input": [1, 5, 2, 3, 4],
            "displayed_expected": [1, 2, 3, 4, 5],
            "domain": "intended",
        },
        {
            "input": [-2, -3, -4, -5, -6],
            "displayed_expected": [-6, -5, -4, -3, -2],
            "domain": "outside-intended-negative-example",
        },
        {
            "input": [1, 0, 2, 3, 4],
            "displayed_expected": [0, 1, 2, 3, 4],
            "domain": "intended",
        },
    ]

    print("DOCUMENTED EXAMPLES")
    for example in documented:
        values = example["input"]
        canonical_result = canonical(values.copy())
        candidate_result = candidate(values.copy())
        record = {
            **example,
            "canonical": canonical_result,
            "candidate": candidate_result,
            "candidate_equals_canonical": candidate_result == canonical_result,
            "canonical_equals_displayed": (
                canonical_result == example["displayed_expected"]
            ),
            "candidate_equals_displayed": (
                candidate_result == example["displayed_expected"]
            ),
        }
        if example["domain"] == "intended":
            record["prose_oracle"] = intended_oracle(values)
            record["candidate_equals_prose_oracle"] = (
                candidate_result == record["prose_oracle"]
            )
        print(json.dumps(record, sort_keys=True))

    named_boundaries = [
        [],
        [0],
        [1],
        [0, 0],
        [1, 1],
        [1, 2],       # equal popcount and <= tie branch
        [2, 1],       # equal popcount and > tie branch
        [1, 3],       # lower popcount branch
        [3, 1],       # higher popcount branch
        [0, 1],
        [1, 0],
        [7, 8, 3, 2, 1, 0],
        [3, 1, 3, 0, 1],
        [2**63 - 1, 2**63, 0, 2**31 - 1, 2**31],
        [2**256 - 1, 2**256, 1, 0],
    ]

    intended_cases: list[list[int]] = [case.copy() for case in named_boundaries]
    exhaustive_values = range(8)
    for length in range(5):
        intended_cases.extend(
            list(values) for values in itertools.product(exhaustive_values, repeat=length)
        )

    rng = random.Random(116_2026)
    boundary_pool = [
        0,
        1,
        2,
        3,
        4,
        7,
        8,
        15,
        16,
        31,
        32,
        63,
        64,
        127,
        128,
        255,
        256,
        2**31 - 1,
        2**31,
        2**63 - 1,
        2**63,
        2**127 - 1,
        2**127,
    ]
    for _ in range(3000):
        length = rng.randrange(0, 15)
        case = [
            (
                rng.choice(boundary_pool)
                if rng.randrange(3) == 0
                else rng.randrange(0, 2**80)
            )
            for _ in range(length)
        ]
        intended_cases.append(case)

    candidate_canonical_mismatches: list[dict[str, object]] = []
    candidate_prose_mismatches: list[dict[str, object]] = []
    for values in intended_cases:
        canonical_result = canonical(values.copy())
        candidate_result = candidate(values.copy())
        oracle_result = intended_oracle(values)
        if candidate_result != canonical_result:
            candidate_canonical_mismatches.append(
                {
                    "input": values,
                    "candidate": candidate_result,
                    "canonical": canonical_result,
                }
            )
        if candidate_result != oracle_result:
            candidate_prose_mismatches.append(
                {
                    "input": values,
                    "candidate": candidate_result,
                    "prose_oracle": oracle_result,
                }
            )

    print("INTENDED-DOMAIN SUMMARY")
    print(f"cases={len(intended_cases)}")
    print(f"candidate_canonical_mismatches={len(candidate_canonical_mismatches)}")
    print(f"candidate_prose_mismatches={len(candidate_prose_mismatches)}")
    if candidate_canonical_mismatches:
        print(
            "first_candidate_canonical_mismatch="
            + json.dumps(candidate_canonical_mismatches[0], sort_keys=True)
        )
    if candidate_prose_mismatches:
        print(
            "first_candidate_prose_mismatch="
            + json.dumps(candidate_prose_mismatches[0], sort_keys=True)
        )

    return 1 if candidate_canonical_mismatches or candidate_prose_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
