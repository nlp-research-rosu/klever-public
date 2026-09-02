#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 135."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/135-can-arrange")


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


def independent_oracle(values: list[Any]) -> int:
    result = -1
    for index in range(1, len(values)):
        if values[index] < values[index - 1]:
            result = index
    return result


def main() -> int:
    canonical = load_entry(SCRATCH / "trusted/canonical.py", "trusted_canonical")
    candidate = load_entry(SCRATCH / "solution.py", "generated_solution")
    integer_cases: list[tuple[str, list[int]]] = [
        ("documented-example-drop", [1, 2, 4, 3, 5]),
        ("documented-example-increasing", [1, 2, 3]),
        ("empty", []),
        ("singleton", [7]),
        ("first-comparison-drop", [1, 0]),
        ("first-comparison-rise", [0, 1]),
        ("drop-at-last", [0, 1, 2, -1]),
        ("all-descending", [5, 4, 3, 2, 1]),
        ("multiple-drops", [9, 2, 8, 1, 7, 0]),
        ("negative-values", [-3, -1, -2, 0, -4]),
        ("large-magnitude", [-(10**100), 0, 10**100, -1]),
    ]

    pool = (-2, -1, 0, 1, 2)
    for length in range(len(pool) + 1):
        for values in itertools.permutations(pool, length):
            integer_cases.append((f"exhaustive-permutation-{length}", list(values)))

    rng = random.Random(135)
    for sample in range(300):
        length = rng.randrange(0, 51)
        values = rng.sample(range(-100_000, 100_001), length)
        integer_cases.append((f"seeded-random-{sample}", values))

    exploratory_orderable_cases: list[tuple[str, list[Any]]] = [
        ("distinct-floats", [1.25, -2.5, 3.75, 0.5]),
        ("distinct-strings", ["ant", "bee", "ape", "zebra", "yak"]),
        ("distinct-tuples", [(0,), (2,), (1,), (3,)]),
    ]

    mismatches: list[tuple[str, list[Any], int, int, int]] = []
    for name, values in integer_cases + exploratory_orderable_cases:
        expected = independent_oracle(values)
        canonical_result = canonical(list(values))
        candidate_result = candidate(list(values))
        if canonical_result != expected or candidate_result != expected:
            mismatches.append(
                (name, values, expected, canonical_result, candidate_result)
            )

    print("ORACLE: independent adjacent-pair scan")
    print(f"INTEGER_CASES: {len(integer_cases)}")
    print("EXHAUSTIVE_INTEGER_SCOPE: every permutation of [-2,-1,0,1,2]")
    print("GENERATED_INTEGER_SCOPE: 300 seed-135 unique lists, lengths 0..50")
    print(f"EXPLORATORY_ORDERABLE_CASES: {len(exploratory_orderable_cases)}")
    print(f"MISMATCHES: {len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH: {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
