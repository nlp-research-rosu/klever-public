#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 128."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prod_signs


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 64

    canonical = load_entry("trusted_canonical", Path(sys.argv[1]))
    generated = load_entry("generated_solution", Path(sys.argv[2]))

    documented_and_boundary = [
        [],
        [1, 2, 2, -4],
        [0, 1],
        [-1],
        [0],
        [1],
        [-1, -2],
        [-1, -2, -3],
        [-1, 0, 1],
        [0, -1],
        [1, 0],
        [-(10**100), 10**100],
        [10**100, 10**100 + 1],
    ]

    checked = 0
    for case in documented_and_boundary:
        expected = canonical(list(case))
        actual = generated(list(case))
        print(f"case={case!r} canonical={expected!r} generated={actual!r}")
        if actual != expected:
            print(f"MISMATCH case={case!r}", file=sys.stderr)
            return 1
        checked += 1

    exhaustive_count = 0
    for length in range(6):
        for values in itertools.product(range(-3, 4), repeat=length):
            case = list(values)
            expected = canonical(case)
            actual = generated(case)
            if actual != expected:
                print(
                    f"MISMATCH exhaustive case={case!r} "
                    f"canonical={expected!r} generated={actual!r}",
                    file=sys.stderr,
                )
                return 1
            exhaustive_count += 1
            checked += 1

    rng = random.Random(128)
    random_count = 500
    for _ in range(random_count):
        length = rng.randrange(0, 65)
        case = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
        expected = canonical(case)
        actual = generated(case)
        if actual != expected:
            print(
                f"MISMATCH random case={case!r} "
                f"canonical={expected!r} generated={actual!r}",
                file=sys.stderr,
            )
            return 1
        checked += 1

    print(
        "SUMMARY "
        f"named={len(documented_and_boundary)} "
        f"exhaustive={exhaustive_count} "
        f"random={random_count} total={checked} mismatches=0"
    )
    print("EXHAUSTIVE_SCOPE lengths=0..5 values=-3..3")
    print("RANDOM_SCOPE seed=128 lengths=0..64 values=-10^12..10^12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
