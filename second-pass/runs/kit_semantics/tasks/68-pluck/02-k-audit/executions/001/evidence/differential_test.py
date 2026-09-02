#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test for HumanEval/68."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


WORK = Path("/tmp/audit-work/68-pluck")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


def expected(arr: list[int]) -> list[int]:
    """Independently restates the natural-language minimum-even/first-index contract."""
    minimum: int | None = None
    minimum_index = 0
    for index, value in enumerate(arr):
        if value % 2 == 0 and (minimum is None or value < minimum):
            minimum = value
            minimum_index = index
    return [] if minimum is None else [minimum, minimum_index]


def main() -> None:
    canonical = load_entry("trusted_canonical", WORK / "canonical.py")
    generated = load_entry("generated_solution", WORK / "solution.py")

    named_cases = {
        "example-1": [4, 2, 3],
        "example-2": [1, 2, 3],
        "example-3-empty": [],
        "example-4-zero-tie": [5, 0, 3, 0, 4, 2],
        "one-odd": [1],
        "one-zero": [0],
        "one-even": [2],
        "first-even-remains": [2, 4],
        "strictly-smaller-replaces": [4, 2],
        "equal-even-preserves-first": [2, 2],
        "odd-after-even": [2, 3],
        "large-integers": [10**100 + 1, 10**100, 2, 0],
        "max-length-all-odd": [1] * 10000,
        "max-length-all-even-tie": [2] * 10000,
        "max-length-ascending": list(range(10000)),
        "max-length-descending": list(reversed(range(10000))),
    }

    checked = 0
    for name, arr in named_cases.items():
        oracle_result = expected(arr)
        canonical_result = canonical(arr)
        generated_result = generated(arr)
        assert canonical_result == oracle_result, (name, canonical_result, oracle_result)
        assert generated_result == oracle_result, (name, generated_result, oracle_result)
        print(f"{name}: len={len(arr)} result={oracle_result}")
        checked += 1

    exhaustive_checked = 0
    for length in range(7):
        for values in itertools.product(range(7), repeat=length):
            arr = list(values)
            oracle_result = expected(arr)
            assert canonical(arr) == oracle_result, arr
            assert generated(arr) == oracle_result, arr
            exhaustive_checked += 1
    checked += exhaustive_checked

    rng = random.Random(6800729)
    random_checked = 0
    for _ in range(2000):
        length = rng.randrange(0, 301)
        arr = [rng.randrange(0, 10**12 + 1) for _ in range(length)]
        oracle_result = expected(arr)
        assert canonical(arr) == oracle_result, arr
        assert generated(arr) == oracle_result, arr
        random_checked += 1
    checked += random_checked

    print("exhaustive_domain=values[0..6], lengths[0..6]")
    print(f"exhaustive_cases={exhaustive_checked}")
    print("random_seed=6800729 random_lengths=0..300 random_values=0..10^12")
    print(f"random_cases={random_checked}")
    print(f"total_cases={checked}")
    print("mismatches=0")


if __name__ == "__main__":
    main()
