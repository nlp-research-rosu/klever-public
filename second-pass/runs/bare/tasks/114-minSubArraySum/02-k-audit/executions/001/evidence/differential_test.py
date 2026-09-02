#!/usr/bin/env python3
"""Independent differential test for HumanEval 114.

Oracle 1 is the trusted mounted canonical implementation.
Oracle 2 is a direct brute-force definition written by the reviewer.
The implementation under test is the candidate solution copied into scratch.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


def brute_force(nums: list[int]) -> int:
    return min(
        sum(nums[start:end])
        for start in range(len(nums))
        for end in range(start + 1, len(nums) + 1)
    )


def check_case(
    nums: list[int],
    canonical,
    candidate,
) -> None:
    trusted = canonical(nums.copy())
    generated = candidate(nums.copy())
    direct = brute_force(nums)
    if trusted != generated or trusted != direct:
        raise AssertionError(
            f"mismatch nums={nums}: canonical={trusted}, "
            f"candidate={generated}, brute_force={direct}"
        )


def exception_name(function, nums: list[int]) -> str:
    try:
        function(nums.copy())
    except Exception as exc:  # boundary behavior is deliberately recorded
        return type(exc).__name__
    return "NO_EXCEPTION"


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: differential_test.py CANONICAL.py SOLUTION.py")
    canonical = load_function(Path(sys.argv[1]), "trusted_canonical")
    candidate = load_function(Path(sys.argv[2]), "generated_solution")

    named_cases = {
        "prompt_positive": [2, 3, 4, 1, 2, 4],
        "prompt_negative": [-1, -2, -3],
        "singleton_negative": [-8],
        "singleton_zero": [0],
        "singleton_positive": [11],
        "length_two_prefix_wins": [-5, 2],
        "length_two_tail_wins": [5, -7],
        "length_two_combined_wins": [-5, -7],
        "equal_branch_boundary": [0, 0],
        "mixed_internal_minimum": [4, -6, 2, -5, 7],
        "large_magnitude": [10**30, -(10**31), 10**30],
    }
    for label, nums in named_cases.items():
        check_case(nums, canonical, candidate)
        print(f"NAMED PASS {label}: {nums} -> {candidate(nums.copy())}")

    exhaustive = 0
    for length in range(1, 6):
        for values in itertools.product(range(-3, 4), repeat=length):
            check_case(list(values), canonical, candidate)
            exhaustive += 1

    rng = random.Random(114)
    generated = 0
    for _ in range(500):
        length = rng.randint(1, 12)
        nums = [rng.randint(-50, 50) for _ in range(length)]
        check_case(nums, canonical, candidate)
        generated += 1

    empty_canonical = exception_name(canonical, [])
    empty_candidate = exception_name(candidate, [])
    print(
        "EMPTY OUTSIDE CONTRACT: "
        f"canonical={empty_canonical}, candidate={empty_candidate}"
    )
    if empty_canonical == "NO_EXCEPTION" or empty_candidate == "NO_EXCEPTION":
        raise AssertionError("an implementation unexpectedly returned on empty input")

    print(
        f"SUMMARY mismatches=0 named={len(named_cases)} "
        f"exhaustive={exhaustive} generated={generated}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
