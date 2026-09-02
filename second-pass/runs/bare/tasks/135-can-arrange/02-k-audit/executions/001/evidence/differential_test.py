#!/usr/bin/env python3
"""Independent canonical-versus-submitted-Python differential test.

The exhaustive corpus uses every permutation without replacement from
[-3, -2, -1, 0, 1, 2, 3].  The generated corpus uses the fixed seed below.
All arrays therefore satisfy the prompt's no-duplicates condition.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Callable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/135-can-arrange/source/solution.py")
CORPUS_PATH = Path("/audit-output/evidence/differential_inputs.jsonl")
SEED = 135_2026_07_23


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


def observed(fn: Callable[[list[int]], int], arr: list[int]) -> dict[str, object]:
    try:
        return {"kind": "return", "value": fn(list(arr))}
    except BaseException as err:  # Exceptions are observable differential results.
        return {"kind": "exception", "type": type(err).__name__, "message": str(err)}


def add_case(
    cases: list[tuple[str, list[int]]],
    seen: set[tuple[int, ...]],
    category: str,
    values: list[int] | tuple[int, ...],
) -> None:
    arr = list(values)
    key = tuple(arr)
    if key not in seen:
        seen.add(key)
        cases.append((category, arr))


def build_cases() -> list[tuple[str, list[int]]]:
    cases: list[tuple[str, list[int]]] = []
    seen: set[tuple[int, ...]] = set()

    curated = [
        ("documented", [1, 2, 4, 3, 5]),
        ("documented", [1, 2, 3]),
        ("empty", []),
        ("singleton", [7]),
        ("length-2-increasing", [-1, 4]),
        ("length-2-drop", [4, -1]),
        ("head-drop-only", [9, 1, 2, 3]),
        ("tail-drop", [1, 2, 5, 3, 4]),
        ("multiple-drops", [9, 1, 8, 2, 7, 3]),
        ("negative-values", [-8, -3, -4, -1]),
        ("large-values", [10**40, 10**50, -(10**60), 10**70]),
    ]
    for category, arr in curated:
        add_case(cases, seen, category, arr)

    pool = (-3, -2, -1, 0, 1, 2, 3)
    for length in range(0, len(pool) + 1):
        for arr in itertools.permutations(pool, length):
            add_case(cases, seen, f"exhaustive-permutation-length-{length}", arr)

    rng = random.Random(SEED)
    population = range(-100_000, 100_001)
    for _ in range(2500):
        length = rng.randrange(0, 65)
        add_case(cases, seen, "generated-seed-135_2026_07_23", rng.sample(population, length))

    # The prompt states no length bound. These cases probe the CPython recursion
    # boundary of the submitted recursive implementation against the iterative
    # trusted implementation.
    for length in range(900, 1051):
        add_case(cases, seen, "recursion-boundary-increasing", list(range(length)))
    add_case(cases, seen, "recursion-boundary-decreasing", list(range(1100, 0, -1)))

    return cases


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical_135")
    generated = load_entry(GENERATED_PATH, "submitted_solution_135")
    cases = build_cases()

    mismatches: list[dict[str, object]] = []
    sha = hashlib.sha256()
    category_counts: dict[str, int] = {}

    with CORPUS_PATH.open("w", encoding="utf-8") as corpus:
        for case_id, (category, arr) in enumerate(cases):
            record = {"id": case_id, "category": category, "arr": arr}
            encoded = json.dumps(record, separators=(",", ":"), sort_keys=True)
            corpus.write(encoded + "\n")
            sha.update((encoded + "\n").encode())
            category_counts[category] = category_counts.get(category, 0) + 1

            expected = observed(canonical, arr)
            actual = observed(generated, arr)
            if actual != expected:
                mismatches.append(
                    {
                        "id": case_id,
                        "category": category,
                        "length": len(arr),
                        "expected": expected,
                        "actual": actual,
                        "prefix": arr[:12],
                    }
                )

    print(
        json.dumps(
            {
                "canonical": str(CANONICAL_PATH),
                "generated": str(GENERATED_PATH),
                "corpus": str(CORPUS_PATH),
                "corpus_sha256": sha.hexdigest(),
                "seed": SEED,
                "case_count": len(cases),
                "category_counts": category_counts,
                "mismatch_count": len(mismatches),
                "first_20_mismatches": mismatches[:20],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
