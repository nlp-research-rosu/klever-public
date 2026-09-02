#!/usr/bin/env python3
"""Independent differential tests for trusted canonical.py vs solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


canonical = load_function("trusted_canonical_58", Path("/reference/canonical.py"))
generated = load_function("generated_solution_58", Path("/tmp/audit-work/58-common-002/solution.py"))


def check(left: list, right: list, label: str) -> None:
    expected = canonical(left.copy(), right.copy())
    actual = generated(left.copy(), right.copy())
    if actual != expected:
        raise AssertionError(
            f"{label}: left={left!r}, right={right!r}, "
            f"canonical={expected!r}, generated={actual!r}"
        )


def all_lists(values: tuple[int, ...], max_len: int):
    yield []
    for length in range(1, max_len + 1):
        for items in itertools.product(values, repeat=length):
            yield list(items)


def main() -> None:
    witness_left = [3, 1, 3, 2]
    witness_right = [2, 3, 2]
    witness_canonical = canonical(witness_left.copy(), witness_right.copy())
    witness_generated = generated(witness_left.copy(), witness_right.copy())
    assert witness_canonical == witness_generated == [2, 3]

    curated = [
        ([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121], "example-1"),
        ([5, 3, 2, 8], [3, 2], "example-2"),
        ([], [], "both-empty"),
        ([], [1], "left-empty"),
        ([1], [], "right-empty"),
        ([1], [2], "membership-false"),
        ([1], [1], "membership-true-first-add"),
        ([1, 1], [1], "duplicate-suppression"),
        ([3, 2, 1], [1, 2, 3], "sort-reorders"),
        ([-10, 0, 10, -10], [10, -10, 99], "negative-and-duplicate"),
        ([True, 1, False, 0, 2], [0, True, 2], "python-bool-int-equality"),
        ([1], [1.0], "python-int-float-equality"),
        (["z", "a", "a"], ["a", "z"], "homogeneous-strings"),
        ([10**100, -(10**100), 7], [7, 10**100], "unbounded-python-ints"),
    ]
    for left, right, label in curated:
        check(left, right, label)

    exhaustive_inputs = list(all_lists((-1, 0, 1), 3))
    exhaustive_pairs = 0
    for left in exhaustive_inputs:
        for right in exhaustive_inputs:
            check(left, right, "exhaustive-small")
            exhaustive_pairs += 1

    rng = random.Random(58002)
    random_cases = 10_000
    for index in range(random_cases):
        left = [rng.randint(-50, 50) for _ in range(rng.randint(0, 20))]
        right = [rng.randint(-50, 50) for _ in range(rng.randint(0, 20))]
        check(left, right, f"random-{index}")

    print(f"curated_cases={len(curated)}")
    print(
        "whole-claim-ground-witness: "
        f"FIRST={witness_left} SECOND={witness_right} "
        "commonSpec-scan=[3, 2] sortVS-result=[2, 3] "
        f"canonical={witness_canonical} generated={witness_generated}"
    )
    print(
        f"exhaustive_lists={len(exhaustive_inputs)} "
        f"exhaustive_pairs={exhaustive_pairs} values=(-1,0,1) max_len=3"
    )
    print(f"deterministic_random_cases={random_cases} seed=58002 values=[-50,50] lengths=[0,20]")
    print("mismatches=0")
    print("DIFFERENTIAL_TEST_OK")


if __name__ == "__main__":
    main()
