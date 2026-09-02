#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/136."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import random
from pathlib import Path
from types import ModuleType


ENTRY_POINT = "largest_smallest_integers"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("generated", type=Path)
    args = parser.parse_args()

    canonical = getattr(load_module("trusted_canonical", args.canonical), ENTRY_POINT)
    generated = getattr(load_module("generated_solution", args.generated), ENTRY_POINT)

    named_cases = [
        [2, 4, 1, 3, 5, 7],
        [],
        [0],
        [-1],
        [1],
        [-3, -1],
        [-1, -3],
        [3, 1],
        [1, 3],
        [-3, -3, -1, -1],
        [3, 3, 1, 1],
        [-2, 0, 2],
        [0, -2, 0, 2, 0],
        [-(10**100), -1, 0, 1, 10**100],
        [10**100, -(10**100)],
    ]

    exhaustive_cases = (
        list(xs)
        for length in range(6)
        for xs in itertools.product(range(-3, 4), repeat=length)
    )

    rng = random.Random(136)
    random_cases = [
        [rng.randint(-10**6, 10**6) for _ in range(rng.randint(0, 50))]
        for _ in range(500)
    ]

    checked = 0
    mismatches = []
    for source, cases in (
        ("named", named_cases),
        ("exhaustive[-3,3],len<=5", exhaustive_cases),
        ("random(seed=136)", random_cases),
    ):
        source_count = 0
        for case in cases:
            expected = canonical(case)
            actual = generated(case)
            checked += 1
            source_count += 1
            if expected != actual:
                mismatches.append((source, case, expected, actual))
                if len(mismatches) >= 20:
                    break
        print(f"source={source} checked={source_count}")
        if mismatches:
            break

    print(f"checked={checked} mismatches={len(mismatches)}")
    for source, case, expected, actual in mismatches:
        print(
            f"MISMATCH source={source} input={case!r} "
            f"canonical={expected!r} generated={actual!r}"
        )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
