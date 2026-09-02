#!/usr/bin/env python3
"""Independent differential and brute-force audit for HumanEval 114."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


TRUSTED_CANONICAL = Path("/reference/canonical.py")
GENERATED_SOLUTION = Path(
    "/tmp/audit-work/review-114.pELioR/candidate-src/solution.py"
)
INPUT_RECORD = Path("/audit-output/evidence/differential-inputs.json")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


def brute_force(nums: list[int]) -> int:
    """Independent definition: minimum sum over every contiguous nonempty slice."""
    return min(
        sum(nums[start:end])
        for start in range(len(nums))
        for end in range(start + 1, len(nums) + 1)
    )


def branch_observations(nums: list[int]) -> set[tuple[bool, bool]]:
    """Record the two source-level If outcomes for candidate control-flow coverage."""
    smallest = nums[0]
    current = 0
    observed: set[tuple[bool, bool]] = set()
    for value in nums:
        current = current + value
        first = value < current
        if first:
            current = value
        second = current < smallest
        if second:
            smallest = current
        observed.add((first, second))
    return observed


def capture_exception(function, value):
    try:
        function(value)
    except Exception as err:  # boundary behavior is part of the record
        return {"type": type(err).__name__, "message": str(err)}
    return {"type": None, "message": None}


def main() -> int:
    canonical = load_entry("trusted_canonical_114", TRUSTED_CANONICAL)
    generated = load_entry("generated_solution_114", GENERATED_SOLUTION)

    documented_and_boundary = [
        [2, 3, 4, 1, 2, 4],
        [-1, -2, -3],
        [5],
        [0],
        [0, 0],
        [1, 2],
        [5, -2],
        [-1, -2],
        [3, -4, 2, -3, -1, 7, -5],
        [7, -7],
        [-7, 7],
        [10**100, -(10**100), 1],
        [-(10**100), 10**100, -1],
    ]

    exhaustive = [
        list(values)
        for length in range(1, 6)
        for values in itertools.product(range(-3, 4), repeat=length)
    ]

    rng = random.Random(114)
    generated_cases = [
        [rng.randint(-1000, 1000) for _ in range(rng.randint(1, 30))]
        for _ in range(500)
    ]

    cases = documented_and_boundary + exhaustive + generated_cases
    mismatches = []
    observed_branches: set[tuple[bool, bool]] = set()
    for index, nums in enumerate(cases):
        oracle = brute_force(nums)
        trusted_result = canonical(list(nums))
        generated_result = generated(list(nums))
        observed_branches.update(branch_observations(nums))
        if trusted_result != oracle or generated_result != oracle:
            mismatches.append(
                {
                    "index": index,
                    "input": nums,
                    "brute_force": oracle,
                    "trusted_canonical": trusted_result,
                    "generated": generated_result,
                }
            )

    empty_input = []
    empty_record = {
        "input": empty_input,
        "trusted_canonical": capture_exception(canonical, empty_input),
        "generated": capture_exception(generated, empty_input),
        "domain_status": "outside nonempty-input contract",
    }

    record = {
        "trusted_canonical_path": str(TRUSTED_CANONICAL),
        "generated_solution_path": str(GENERATED_SOLUTION),
        "documented_and_boundary": documented_and_boundary,
        "exhaustive_generator": {
            "lengths": [1, 2, 3, 4, 5],
            "element_values": [-3, -2, -1, 0, 1, 2, 3],
            "expanded_cases": exhaustive,
        },
        "random_generator": {
            "seed": 114,
            "case_count": 500,
            "length_range": [1, 30],
            "element_range": [-1000, 1000],
            "expanded_cases": generated_cases,
        },
        "empty_boundary": empty_record,
    }
    INPUT_RECORD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    expected_branch_pairs = {
        (False, False),
        (False, True),
        (True, False),
        (True, True),
    }
    print(f"nonempty_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    print(f"branch_pairs={sorted(observed_branches)}")
    print(f"all_branch_pairs_seen={observed_branches == expected_branch_pairs}")
    print(f"empty_boundary={json.dumps(empty_record, sort_keys=True)}")
    print(f"input_record={INPUT_RECORD}")

    if mismatches:
        print(json.dumps(mismatches[:20], indent=2))
        return 1
    if observed_branches != expected_branch_pairs:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
