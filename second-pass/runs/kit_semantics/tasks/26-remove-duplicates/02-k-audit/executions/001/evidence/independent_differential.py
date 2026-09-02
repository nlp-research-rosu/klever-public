#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/26."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("generated", type=Path)
    args = parser.parse_args()

    canonical = load_function(args.canonical, "trusted_canonical")
    generated = load_function(args.generated, "candidate_generated")

    named_cases = [
        ("documented-example", [1, 2, 3, 2, 4]),
        ("empty", []),
        ("singleton-append-branch", [0]),
        ("pair-skip-boundary", [7, 7]),
        ("triple-skip", [7, 7, 7]),
        ("unique-around-duplicate", [1, 2, 1, 3]),
        ("several-multiplicities", [-1, 0, -1, 2, 2, 3, 4, 4, 4]),
        ("large-unbounded-integers", [10**100, -(10**100), 10**100, 5]),
        ("all-unique-order", [3, -2, 0, 9]),
        ("all-repeated", [1, 2, 1, 2]),
    ]

    mismatches = []
    checked = 0

    def rd_acc(acc: list[int], rest: list[int], all_values: list[int]) -> list[int]:
        result = list(acc)
        for value in rest:
            if sum(1 for candidate in all_values if candidate == value) == 1:
                result.append(value)
        return result

    def check(case_name: str, values: list[int]) -> None:
        nonlocal checked
        expected_input = copy.deepcopy(values)
        actual_input = copy.deepcopy(values)
        expected = canonical(expected_input)
        actual = generated(actual_input)
        claimed = rd_acc([], values, values)
        checked += 1
        if (
            expected != actual
            or claimed != expected
            or expected_input != values
            or actual_input != values
        ):
            mismatches.append(
                {
                    "case": case_name,
                    "input": values,
                    "canonical": expected,
                    "generated": actual,
                    "claimed_rdAcc": claimed,
                    "canonical_input_after": expected_input,
                    "generated_input_after": actual_input,
                }
            )
        if case_name.startswith(("documented", "empty", "singleton", "pair", "triple")):
            print(
                f"{case_name}: input={values!r} canonical={expected!r} "
                f"generated={actual!r} rdAcc={claimed!r}"
            )

    for name, values in named_cases:
        check(name, values)

    alphabet = [-2, -1, 0, 1, 2]
    exhaustive_count = 0
    for length in range(7):
        for values in itertools.product(alphabet, repeat=length):
            check(f"exhaustive-length-{length}", list(values))
            exhaustive_count += 1

    rng = random.Random(260726)
    random_count = 3000
    for index in range(random_count):
        length = rng.randrange(0, 61)
        values = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
        if length >= 2 and index % 3 == 0:
            values[-1] = values[0]
        if length >= 4 and index % 5 == 0:
            values[-2] = values[1]
        check(f"random-{index}", values)

    print(f"named cases: {len(named_cases)}")
    print(f"exhaustive cases: {exhaustive_count}")
    print(f"random cases: {random_count}")
    print(f"total cases: {checked}")
    print(f"mismatches: {len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:10]:
            print(mismatch)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
