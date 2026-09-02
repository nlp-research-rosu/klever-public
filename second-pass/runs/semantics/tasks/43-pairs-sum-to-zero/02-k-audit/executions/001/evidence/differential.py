#!/usr/bin/env python3
"""Independent differential test for HumanEval 43.

The candidate and trusted canonical modules are loaded from explicit paths.  The
input family is reproducible: documented and hand-picked boundary cases, all
lists of length 0..6 over [-2, -1, 0, 1, 2], and 1,000 pseudorandom integer
lists generated with seed 430043.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/pairs-audit/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero


def independent_contract(values: list[int]) -> bool:
    return any(
        values[i] + values[j] == 0
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )


DOCUMENTED = [
    [1, 3, 5, 0],
    [1, 3, -2, 1],
    [1, 2, 3, 7],
    [2, 4, -5, 3, 5, 7],
    [1],
]

BOUNDARIES = [
    [],
    [0],
    [0, 0],
    [1, -1],
    [-1, 1],
    [1, 1],
    [-1, -1],
    [2, 0, -2],
    [2, -2, 999],
    [999, 2, -2],
    [-8, 3, 8],
    [-(10**100), 4, 10**100],
    [10**100, -(10**100)],
    [5, -5, 5, -5],
]


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    generated = load_entry(GENERATED_PATH, "generated_solution")
    mismatches: list[tuple[list[int], bool, bool, bool]] = []
    count = 0

    def check(values: list[int]) -> None:
        nonlocal count
        expected = independent_contract(values)
        canonical_result = canonical(values.copy())
        generated_result = generated(values.copy())
        count += 1
        if not (
            type(canonical_result) is bool
            and type(generated_result) is bool
            and canonical_result == generated_result == expected
        ):
            mismatches.append(
                (values, expected, canonical_result, generated_result)
            )

    for values in DOCUMENTED:
        check(values)
    for values in BOUNDARIES:
        check(values)

    alphabet = [-2, -1, 0, 1, 2]
    exhaustive_count = 0
    for length in range(7):
        for values in itertools.product(alphabet, repeat=length):
            check(list(values))
            exhaustive_count += 1

    rng = random.Random(430043)
    random_count = 1_000
    for _ in range(random_count):
        length = rng.randrange(0, 31)
        values = [rng.randrange(-10**6, 10**6 + 1) for _ in range(length)]
        if length >= 2 and rng.random() < 0.5:
            left, right = rng.sample(range(length), 2)
            values[right] = -values[left]
        check(values)

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print(f"documented_count={len(DOCUMENTED)}")
    print(f"boundary_count={len(BOUNDARIES)}")
    print(
        "exhaustive_scope=lengths 0..6 over alphabet "
        "[-2,-1,0,1,2]"
    )
    print(f"exhaustive_count={exhaustive_count}")
    print("random_seed=430043")
    print("random_scope=1000 lists, lengths 0..30, values -1000000..1000000")
    print(f"random_count={random_count}")
    print(f"total_count={count}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
