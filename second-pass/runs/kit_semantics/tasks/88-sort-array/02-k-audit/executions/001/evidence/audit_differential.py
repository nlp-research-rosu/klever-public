#!/usr/bin/env python3
"""Independent differential test for HumanEval 88 sort_array."""

from __future__ import annotations

import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import random
from types import ModuleType


ROOT = Path("/tmp/audit-work/reconstruction")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_contract(values: list[int]) -> list[int]:
    if not values:
        return []
    ascending = sorted(values)
    if (values[0] + values[-1]) % 2 == 1:
        return ascending
    return list(reversed(ascending))


def main() -> None:
    canonical = load_module("trusted_canonical_88", ROOT / "canonical.py")
    candidate = load_module("generated_solution_88", ROOT / "solution.py")

    documented_and_boundaries = [
        [],
        [5],
        [2, 4, 3, 0, 1, 5],
        [2, 4, 3, 0, 1, 5, 6],
        [0],
        [1],
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
        [2, 3],
        [3, 2],
        [7, 7, 7],
        [0, 2, 1, 2],
        [10**80, 0, 10**80 + 1],
        [10**80 + 1, 0, 10**80 + 1],
    ]
    exhaustive = [
        list(values)
        for length in range(6)
        for values in product(range(5), repeat=length)
    ]
    rng = random.Random(880088)
    generated = [
        [rng.randrange(0, 10**12) for _ in range(rng.randrange(0, 31))]
        for _ in range(500)
    ]

    cases: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for case in documented_and_boundaries + exhaustive + generated:
        key = tuple(case)
        if key not in seen:
            seen.add(key)
            cases.append(case)

    odd_branch = 0
    even_branch = 0
    empty_branch = 0
    for index, values in enumerate(cases):
        original = list(values)
        candidate_input = list(values)
        canonical_input = list(values)
        candidate_result = candidate.sort_array(candidate_input)
        canonical_result = canonical.sort_array(canonical_input)
        expected = independent_contract(values)

        assert candidate_result == canonical_result == expected, (
            index,
            values,
            candidate_result,
            canonical_result,
            expected,
        )
        assert candidate_input == original
        assert canonical_input == original
        assert candidate_result is not candidate_input
        assert canonical_result is not canonical_input

        if not values:
            empty_branch += 1
        elif (values[0] + values[-1]) % 2:
            odd_branch += 1
        else:
            even_branch += 1

    case_digest = hashlib.sha256(
        json.dumps(cases, separators=(",", ":")).encode()
    ).hexdigest()
    print(
        "DIFFERENTIAL_RESULT PASS "
        f"cases={len(cases)} empty={empty_branch} "
        f"odd={odd_branch} even={even_branch} "
        f"case_sha256={case_digest}"
    )


if __name__ == "__main__":
    main()
