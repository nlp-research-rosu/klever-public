#!/usr/bin/env python3
"""Independent differential test for HumanEval 68-pluck.

Oracle: the trusted, unmodified canonical.py mount.
Implementation: the submitted solution.py copied into scratch.
Domain: finite lists of non-negative Python integers, including the explicitly
documented empty case and the stated maximum length of 10,000.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py CANONICAL.py SOLUTION.py")
        return 2
    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
    generated = load_entry(Path(sys.argv[2]), "generated_solution")

    named_cases = [
        ("example-1", [4, 2, 3], [2, 1]),
        ("example-2", [1, 2, 3], [2, 1]),
        ("example-3-empty", [], []),
        ("example-4-duplicate-zero", [5, 0, 3, 0, 4, 2], [0, 1]),
        ("single-even-zero", [0], [0, 0]),
        ("single-even-positive", [2], [2, 0]),
        ("single-odd", [1], []),
        ("all-odd", [1, 3, 5, 7], []),
        ("equal-even-first-index", [4, 4, 4], [4, 0]),
        ("smaller-even-last", [8, 6, 4, 2], [2, 3]),
        ("zero-last", [9, 7, 0], [0, 2]),
        ("large-values", [10**100 + 1, 10**100, 2], [2, 2]),
        ("max-length-no-even", [1] * 10_000, []),
        ("max-length-last-even", [1] * 9_999 + [2], [2, 9_999]),
        ("max-length-tied-min", [8] + [3] * 9_998 + [8], [8, 0]),
    ]

    checked = 0
    digest = hashlib.sha256()

    def check(label: str, arr: list[int], expected=None) -> None:
        nonlocal checked
        oracle = canonical(arr)
        actual = generated(arr)
        if expected is not None and oracle != expected:
            raise AssertionError(
                f"trusted oracle disagrees with documented case {label}: "
                f"{oracle!r} != {expected!r}"
            )
        if actual != oracle:
            raise AssertionError(
                f"mismatch {label}: input={arr!r} canonical={oracle!r} "
                f"generated={actual!r}"
            )
        checked += 1
        digest.update(
            json.dumps(
                [label, arr, oracle], separators=(",", ":"), sort_keys=True
            ).encode()
        )

    print("named_cases:")
    for label, arr, expected in named_cases:
        check(label, arr, expected)
        print(f"  {label}: len={len(arr)} result={generated(arr)!r}")

    # Exhaustive small coverage crosses every parity/minimum/tie/position branch.
    exhaustive = 0
    for length in range(0, 7):
        for values in itertools.product(range(8), repeat=length):
            check(f"exhaustive-{length}", list(values))
            exhaustive += 1

    # Deterministic broader samples include large lengths and arbitrary-size ints.
    rng = random.Random(680026)
    random_cases = 2_000
    for case_index in range(random_cases):
        if case_index < 100:
            length = rng.randrange(0, 10_001)
        else:
            length = rng.randrange(0, 81)
        arr = [rng.randrange(0, 10**12) for _ in range(length)]
        check(f"random-{case_index}", arr)

    print(f"exhaustive_cases={exhaustive}")
    print(f"random_cases={random_cases}")
    print(f"total_cases={checked}")
    print(f"case_result_sha256={digest.hexdigest()}")
    print("mismatches=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
