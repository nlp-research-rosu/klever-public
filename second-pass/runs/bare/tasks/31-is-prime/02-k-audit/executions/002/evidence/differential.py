#!/usr/bin/env python3
"""Independent CPython differential for HumanEval/31."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime


def outcome(function, value: int):
    try:
        return ("return", function(value))
    except BaseException as error:  # Exceptions are observable differential outcomes.
        return ("raise", type(error).__name__, str(error))


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: differential.py CANONICAL.py SOLUTION.py")

    canonical = load_function("trusted_canonical", Path(sys.argv[1]))
    generated = load_function("generated_solution", Path(sys.argv[2]))

    examples = [6, 101, 11, 13441, 61, 4, 1]
    branch_boundaries = [
        -10, -1, 0, 1, 2, 3, 4, 5,
        8, 9, 10, 15, 16, 17, 24, 25, 26, 48, 49, 50,
    ]
    exhaustive_small = list(range(-25, 501))
    rng = random.Random(310031)
    generated_sample = [rng.randint(-1_000, 100_000) for _ in range(250)]
    recursion_boundaries = [9973, 99991, 1_000_003]

    groups = [
        ("documented examples", examples),
        ("empty/not-applicable and branch boundaries", branch_boundaries),
        ("exhaustive integer interval", exhaustive_small),
        ("seeded representative integers", generated_sample),
        ("CPython recursion-depth boundary probes", recursion_boundaries),
    ]

    mismatches = []
    total = 0
    for label, values in groups:
        print(f"GROUP {label}: count={len(values)}")
        for value in values:
            total += 1
            expected = outcome(canonical, value)
            actual = outcome(generated, value)
            if expected != actual:
                mismatches.append((label, value, expected, actual))
                print(
                    f"MISMATCH group={label!r} n={value} "
                    f"canonical={expected!r} generated={actual!r}"
                )

    print(f"TOTAL_CASES={total}")
    print(f"MISMATCHES={len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
