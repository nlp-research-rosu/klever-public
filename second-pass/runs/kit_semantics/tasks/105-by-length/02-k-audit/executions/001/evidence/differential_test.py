#!/usr/bin/env python3
"""Independent differential test for HumanEval/105 over integer-list inputs."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
from pathlib import Path
import random
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.by_length


def outcome(function: Callable[[list[int]], list[str]], values: list[int]) -> tuple[str, object]:
    try:
        return ("return", function(values))
    except BaseException as error:  # Compare exceptional behavior as well as values.
        return ("raise", (type(error).__name__, str(error)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("generated", type=Path)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    generated = load_entry(args.generated, "generated_solution")

    named_cases = [
        ("documented-main", [2, 1, 1, 4, 5, 8, 2, 3]),
        ("documented-empty", []),
        ("documented-strange", [1, -1, 55]),
        ("lower-bound-miss", [0]),
        ("lower-bound-hit", [1]),
        ("upper-bound-hit", [9]),
        ("upper-bound-miss", [10]),
        ("all-digit-branches", list(range(1, 10))),
        ("descending", list(range(9, 0, -1))),
        ("duplicates-and-misses", [9, 0, 9, 10, 1, 1, -7, 5]),
        ("large-magnitudes", [-(10**100), 1, 9, 10**100]),
        ("repeated-boundaries", [0, 1, 1, 9, 9, 10]),
    ]
    alphabet = [-100, -1, 0, 1, 2, 8, 9, 10, 55]
    exhaustive_cases = (
        list(product)
        for length in range(5)
        for product in itertools.product(alphabet, repeat=length)
    )
    rng = random.Random(105_2026_07_29)
    random_cases = [
        [rng.randint(-(10**9), 10**9) for _ in range(rng.randint(0, 60))]
        for _ in range(10_000)
    ]

    mismatches: list[tuple[str, list[int], object, object]] = []
    checked = 0
    for label, values in named_cases:
        original = values.copy()
        left = outcome(canonical, values)
        canonical_mutated = values != original
        values[:] = original
        right = outcome(generated, values)
        generated_mutated = values != original
        checked += 1
        print(
            f"named {label}: input={original!r} canonical={left!r} generated={right!r} "
            f"canonical_mutated={canonical_mutated} generated_mutated={generated_mutated}"
        )
        if left != right or canonical_mutated or generated_mutated:
            mismatches.append((label, original, left, right))

    for values in exhaustive_cases:
        original = values.copy()
        left = outcome(canonical, values)
        right = outcome(generated, values)
        checked += 1
        if left != right or values != original:
            mismatches.append(("exhaustive", original, left, right))
            if len(mismatches) >= 20:
                break

    if len(mismatches) < 20:
        for values in random_cases:
            original = values.copy()
            left = outcome(canonical, values)
            right = outcome(generated, values)
            checked += 1
            if left != right or values != original:
                mismatches.append(("random", original, left, right))
                if len(mismatches) >= 20:
                    break

    print(
        "scope: 12 named cases; all lists of lengths 0..4 over "
        f"{alphabet!r}; 10,000 seeded random lists of lengths 0..60"
    )
    print(f"checked={checked} mismatches={len(mismatches)}")
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
