#!/usr/bin/env python3
"""Independent source-level differential test for HumanEval/73."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path
from typing import Callable


SCRATCH = Path("/tmp/audit-work/73-smallest-change")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


def independent_pair_oracle(values: list[int]) -> int:
    """Count unequal mirrored pairs without using either implementation."""
    return sum(
        1 for left, right in zip(values, reversed(values)) if left != right
    ) // 2


def main() -> int:
    canonical = load_entry(SCRATCH / "trusted-canonical.py", "trusted_canonical")
    generated = load_entry(SCRATCH / "solution.py", "generated_solution")

    documented_and_boundaries = [
        [],
        [7],
        [1, 1],
        [1, 2],
        [1, 2, 1],
        [1, 2, 3],
        [1, 2, 2, 1],
        [1, 2, 3, 1],
        [1, 2, 3, 5, 4, 7, 9, 6],
        [1, 2, 3, 4, 3, 2, 2],
        [1, 2, 3, 2, 1],
        [-1, 0, -1],
        [-2**63, 2**63 - 1],
        [10**100, 0, -(10**100), 10**100],
    ]

    mismatches: list[tuple[list[int], int, int, int]] = []
    checked = 0

    def check(values: list[int]) -> None:
        nonlocal checked
        trusted_result = canonical(values)
        generated_result = generated(values)
        direct_result = independent_pair_oracle(values)
        checked += 1
        if not (trusted_result == generated_result == direct_result):
            mismatches.append(
                (values.copy(), trusted_result, generated_result, direct_result)
            )

    for values in documented_and_boundaries:
        check(values)

    exhaustive_values = (-2, -1, 0, 1, 2)
    exhaustive_max_length = 7
    exhaustive_count = 0
    for length in range(exhaustive_max_length + 1):
        for values in itertools.product(exhaustive_values, repeat=length):
            check(list(values))
            exhaustive_count += 1

    random_seed = 730073
    random_count = 1000
    generator = random.Random(random_seed)
    for _ in range(random_count):
        length = generator.randrange(0, 101)
        values = [
            generator.choice(
                (
                    generator.randint(-10**9, 10**9),
                    -(10**100),
                    -1,
                    0,
                    1,
                    10**100,
                )
            )
            for _ in range(length)
        ]
        check(values)

    print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
    print(f"exhaustive_value_set={exhaustive_values}")
    print(f"exhaustive_lengths=0..{exhaustive_max_length}")
    print(f"exhaustive_cases={exhaustive_count}")
    print(f"random_seed={random_seed}")
    print(f"random_cases={random_count}")
    print("random_lengths=0..100")
    print(f"total_cases={checked}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print(f"MISMATCH={mismatch!r}")
        return 1
    print("RESULT: all trusted-canonical, generated, and independent-oracle outputs agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
