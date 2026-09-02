#!/usr/bin/env python3
"""Independent differential and mathematical-oracle test for HumanEval/31."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
import sys
from pathlib import Path


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mathematical_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % divisor != 0 for divisor in range(2, math.isqrt(n) + 1))


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: differential_test.py CANONICAL.py SOLUTION.py INPUTS.json"
        )
    canonical_path = Path(sys.argv[1]).resolve()
    solution_path = Path(sys.argv[2]).resolve()
    inputs_path = Path(sys.argv[3]).resolve()

    canonical = import_module(canonical_path, "trusted_canonical")
    solution = import_module(solution_path, "submitted_solution")

    prompt_examples = [6, 101, 11, 13441, 61, 4, 1]
    branch_boundaries = [
        -10,
        -3,
        -1,
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        15,
        16,
        17,
        24,
        25,
        26,
        35,
        36,
        37,
        48,
        49,
        50,
        120,
        121,
        122,
        99991,
        99999,
        100000,
    ]
    exhaustive_small = list(range(-100, 5001))
    rng = random.Random(310031)
    deterministic_sample = [rng.randint(-100_000, 100_000) for _ in range(2000)]
    inputs = list(
        dict.fromkeys(
            prompt_examples
            + branch_boundaries
            + exhaustive_small
            + deterministic_sample
        )
    )
    serialized = json.dumps(inputs, indent=2) + "\n"
    inputs_path.write_text(serialized)

    mismatches: list[dict[str, object]] = []
    for n in inputs:
        expected = canonical.is_prime(n)
        actual = solution.is_prime(n)
        oracle = mathematical_prime(n)
        if (
            type(expected) is not bool
            or type(actual) is not bool
            or expected != actual
            or expected != oracle
        ):
            mismatches.append(
                {
                    "n": n,
                    "canonical": expected,
                    "solution": actual,
                    "math_oracle": oracle,
                    "canonical_type": type(expected).__name__,
                    "solution_type": type(actual).__name__,
                }
            )

    encoded = serialized.encode()
    print(f"canonical={canonical_path}")
    print(f"solution={solution_path}")
    print("domain=Python integers")
    print(f"prompt_examples={prompt_examples}")
    print(f"branch_boundaries={branch_boundaries}")
    print("exhaustive_small=[-100,5000]")
    print("deterministic_random_seed=310031")
    print("deterministic_random_count=2000 range=[-100000,100000]")
    print(f"unique_input_count={len(inputs)}")
    print(f"input_file={inputs_path}")
    print(f"input_file_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:100], indent=2, sort_keys=True))
        return 1
    print("RESULT: all canonical, submitted, and independent-oracle outputs agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
