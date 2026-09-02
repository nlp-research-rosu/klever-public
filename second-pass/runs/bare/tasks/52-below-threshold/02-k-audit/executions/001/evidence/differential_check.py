#!/usr/bin/env python3
"""Independent differential and mathematical-oracle check for HumanEval 52."""

from __future__ import annotations

import importlib.util
import inspect
import itertools
import pathlib
import random
import sys
from collections.abc import Callable


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[list[int], int], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot create module spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "below_threshold")
    if not callable(entry):
        raise TypeError(f"{path}: below_threshold is not callable")
    return entry


def oracle(values: list[int], threshold: int) -> bool:
    return all(value < threshold for value in values)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED_CANONICAL.py GENERATED.py", file=sys.stderr)
        return 64

    canonical_path = pathlib.Path(sys.argv[1]).resolve()
    generated_path = pathlib.Path(sys.argv[2]).resolve()
    canonical = load_entry(canonical_path, "audit_trusted_canonical")
    generated = load_entry(generated_path, "audit_generated_solution")

    print(f"trusted canonical: {canonical_path}")
    print(f"generated solution: {generated_path}")
    print(f"canonical signature: {inspect.signature(canonical)}")
    print(f"generated signature: {inspect.signature(generated)}")

    documented_and_boundary_cases = [
        ("prompt true", [1, 2, 4, 10], 100),
        ("prompt false", [1, 20, 4, 10], 5),
        ("empty", [], 0),
        ("empty negative threshold", [], -100),
        ("singleton just below", [4], 5),
        ("singleton equal", [5], 5),
        ("singleton just above", [6], 5),
        ("failure first", [5, -100, -200], 5),
        ("failure middle", [-100, 5, -200], 5),
        ("failure last", [-100, -200, 5], 5),
        ("all negative below", [-5, -4, -3], -2),
        ("negative equality", [-5, -4, -3], -4),
        ("large integers true", [-(10**100), 10**100], 10**101),
        ("large integer equality", [10**100], 10**100),
        ("duplicates true", [2, 2, 2], 3),
        ("duplicates false", [3, 3, 3], 3),
    ]

    mismatch_count = 0
    total_count = 0

    def check(label: str, values: list[int], threshold: int, verbose: bool = False) -> None:
        nonlocal mismatch_count, total_count
        expected = oracle(values, threshold)
        canonical_result = canonical(list(values), threshold)
        generated_result = generated(list(values), threshold)
        total_count += 1
        good = (
            type(canonical_result) is bool
            and type(generated_result) is bool
            and canonical_result == generated_result == expected
        )
        if verbose or not good:
            print(
                f"{label}: l={values!r}, t={threshold!r}, "
                f"canonical={canonical_result!r}, generated={generated_result!r}, "
                f"oracle={expected!r}, ok={good}"
            )
        if not good:
            mismatch_count += 1

    for label, values, threshold in documented_and_boundary_cases:
        check(label, values, threshold, verbose=True)

    exhaustive_values = range(-4, 5)
    exhaustive_thresholds = range(-3, 4)
    exhaustive_count = 0
    for length in range(5):
        for values_tuple in itertools.product(exhaustive_values, repeat=length):
            for threshold in exhaustive_thresholds:
                check("exhaustive", list(values_tuple), threshold)
                exhaustive_count += 1

    rng = random.Random(520052)
    random_count = 2500
    for _ in range(random_count):
        length = rng.randrange(0, 31)
        values = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
        threshold = rng.randrange(-(10**12), 10**12 + 1)
        check("generated", values, threshold)

    print(f"documented/boundary cases: {len(documented_and_boundary_cases)}")
    print(
        "exhaustive scope: list lengths 0..4, elements -4..4, "
        f"thresholds -3..3 ({exhaustive_count} cases)"
    )
    print(
        "generated scope: seed 520052, 2500 lists, lengths 0..30, "
        "integer elements and thresholds in [-10^12, 10^12]"
    )
    print(f"total cases: {total_count}")
    print(f"mismatches: {mismatch_count}")
    return 0 if mismatch_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
