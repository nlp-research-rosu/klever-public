#!/usr/bin/env python3
"""Independent differential test for HumanEval 9 rolling_max."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/rolling-max-20260729/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rolling_max


def main() -> int:
    canonical = load_function("trusted_canonical", CANONICAL_PATH)
    generated = load_function("candidate_generated", GENERATED_PATH)

    documented_and_boundaries = [
        [],
        [0],
        [1],
        [-1],
        [1, 2, 3, 2, 3, 4, 2],
        [1, 0],          # comparison false
        [1, 1],          # equality boundary
        [1, 2],          # comparison true
        [3, 2, 1],       # always false after initialization
        [-3, -2, -1],    # true branch over negatives
        [-1, -2, -2, 0],
        [5, 5, 5, 5],
        [-(10**100), 0, 10**100, -(10**200)],
        [10**300, -(10**300), 10**301],
    ]

    exhaustive_values = (-3, -1, 0, 1, 3)
    exhaustive = (
        list(values)
        for length in range(0, 7)
        for values in itertools.product(exhaustive_values, repeat=length)
    )

    rng = random.Random(0x09A0D17)
    random_cases: list[list[int]] = []
    edge_pool = [
        -(10**200),
        -(2**63),
        -(2**31),
        -1,
        0,
        1,
        2**31 - 1,
        2**63 - 1,
        10**200,
    ]
    for _ in range(2000):
        length = rng.randrange(0, 101)
        case = []
        for _ in range(length):
            if rng.randrange(4) == 0:
                case.append(rng.choice(edge_pool))
            else:
                case.append(rng.randrange(-(10**30), 10**30 + 1))
        random_cases.append(case)

    groups = [
        ("documented_and_boundaries", iter(documented_and_boundaries)),
        ("exhaustive_lengths_0_through_6_values_-3_-1_0_1_3", exhaustive),
        ("seeded_random_2000_lengths_0_through_100", iter(random_cases)),
    ]

    count = 0
    mismatches: list[tuple[str, list[int], object, object]] = []
    for group_name, cases in groups:
        group_count = 0
        for case in cases:
            expected = canonical(list(case))
            actual = generated(list(case))
            count += 1
            group_count += 1
            if actual != expected:
                mismatches.append((group_name, case, expected, actual))
                if len(mismatches) >= 20:
                    break
        print(f"group={group_name} cases={group_count}")
        if mismatches:
            break

    print(f"total_cases={count}")
    print(f"mismatches={len(mismatches)}")
    for group_name, case, expected, actual in mismatches:
        print(
            f"MISMATCH group={group_name} input={case!r} "
            f"canonical={expected!r} generated={actual!r}"
        )
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
