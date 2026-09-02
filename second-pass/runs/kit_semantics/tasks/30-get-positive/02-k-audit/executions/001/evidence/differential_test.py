#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from typing import Callable


def load_function(path: Path) -> Callable[[list], list]:
    spec = importlib.util.spec_from_file_location(f"audited_{path.stem}_{id(path)}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


def encode_number(value: int | float) -> tuple[str, str]:
    if isinstance(value, float) and math.isnan(value):
        return ("float", "nan")
    if isinstance(value, float) and math.isinf(value):
        return ("float", "inf" if value > 0 else "-inf")
    return (type(value).__name__, repr(value))


def encode_result(result: list) -> list[tuple[str, str]]:
    return [encode_number(value) for value in result]


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"))
    generated = load_function(Path("/candidate/solution.py"))

    fixed_cases: list[list[int | float]] = [
        [-1, 2, -4, 5, 6],
        [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
        [],
        [0],
        [0.0],
        [-0.0],
        [-1],
        [1],
        [-1.0],
        [1.0],
        [-(2**63), 2**63 - 1],
        [-(10**100), 10**100],
        [float("-inf"), -5e-324, -0.0, 0, 0.0, 5e-324, float("inf")],
        [float("nan"), -1, 0, 1],
        [1, -1, 2, -2, 3, -3],
        [-3, -2, -1, 0],
        [1, 2, 3],
    ]

    pool: list[int | float] = [
        -(10**100), -(2**63), -1000, -2, -1, -1.0, -5e-324,
        -0.0, 0, 0.0, 5e-324, 0.5, 1, 1.0, 2, 1000,
        2**63 - 1, 10**100, float("-inf"), float("inf"), float("nan"),
    ]
    rng = random.Random(30030)
    generated_cases = [
        [rng.choice(pool) for _ in range(rng.randrange(0, 41))]
        for _ in range(1000)
    ]
    cases = fixed_cases + generated_cases

    mismatches = []
    for index, case in enumerate(cases):
        expected = encode_result(canonical(list(case)))
        actual = encode_result(generated(list(case)))
        if expected != actual:
            mismatches.append((index, case, expected, actual))

    print(f"ORACLE=/reference/canonical.py:get_positive")
    print(f"GENERATED=/candidate/solution.py:get_positive")
    print(f"FIXED_CASES={len(fixed_cases)}")
    print(f"RANDOM_SEED=30030")
    print(f"GENERATED_CASES={len(generated_cases)}")
    print(f"TOTAL_CASES={len(cases)}")
    print("FIXED_INPUTS:")
    for index, case in enumerate(fixed_cases):
        print(f"  {index}: {case!r}")
    print(f"MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={mismatch!r}")
    return int(bool(mismatches))


if __name__ == "__main__":
    raise SystemExit(main())
