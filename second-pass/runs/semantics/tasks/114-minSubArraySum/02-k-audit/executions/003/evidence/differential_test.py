#!/usr/bin/env python3
"""Independent fidelity checks for HumanEval 114.

The intended result domain is non-empty lists of Python integers.  The empty
list is exercised and reported separately because no non-empty subarray exists.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable

SCRATCH = Path("/tmp/audit-work/114-minSubArraySum")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


canonical = load_entry(SCRATCH / "canonical.py", "trusted_canonical_114")
candidate = load_entry(SCRATCH / "solution.py", "generated_solution_114")


def brute_force(nums: list[int]) -> int:
    assert nums
    return min(
        sum(nums[start:stop])
        for start in range(len(nums))
        for stop in range(start + 1, len(nums) + 1)
    )


def outcome(fn: Callable[[list[int]], int], arg: list[int]) -> tuple[str, str]:
    try:
        return ("return", repr(fn(arg)))
    except Exception as err:
        return ("raise", f"{type(err).__name__}: {err}")


documented = [
    [2, 3, 4, 1, 2, 4],
    [-1, -2, -3],
]
boundaries = [
    [0],
    [1],
    [-1],
    [0, 0],
    [1, 1],
    [-1, -1],
    [1, -1],
    [-1, 1],
    [2, -2, 2],
    [-2, 2, -2],
    [5, -4, -1, 2, -7, 3],
    [10**100],
    [10**100, -(10**100), -1, 10**100],
    [-(10**100), 10**100, -(10**100)],
]

branch_relations: dict[str, set[str]] = {
    "value_vs_extended_current": set(),
    "current_vs_smallest": set(),
}


def relation(left: int, right: int) -> str:
    if left < right:
        return "LT"
    if left == right:
        return "EQ"
    return "GT"


def observe_candidate_branches(nums: list[int]) -> None:
    smallest = nums[0]
    current = 0
    for value in nums:
        extended = current + value
        branch_relations["value_vs_extended_current"].add(relation(value, extended))
        current = value if value < extended else extended
        branch_relations["current_vs_smallest"].add(relation(current, smallest))
        if current < smallest:
            smallest = current


checked = 0


def check(nums: list[int], label: str) -> None:
    global checked
    expected = canonical(nums.copy())
    actual = candidate(nums.copy())
    independent = brute_force(nums)
    assert actual == expected == independent, (
        label,
        nums,
        actual,
        expected,
        independent,
    )
    observe_candidate_branches(nums)
    checked += 1


for case in documented:
    check(case, "documented")
for case in boundaries:
    check(case, "boundary")

exhaustive_checked = 0
for length in range(1, 7):
    for values in itertools.product(range(-3, 4), repeat=length):
        check(list(values), f"exhaustive-length-{length}")
        exhaustive_checked += 1

rng = random.Random(11420260726)
random_checked = 0
for _ in range(5000):
    length = rng.randint(1, 30)
    values = [rng.randint(-(10**12), 10**12) for _ in range(length)]
    check(values, "deterministic-random")
    random_checked += 1

empty_canonical = outcome(canonical, [])
empty_candidate = outcome(candidate, [])

print(f"documented_cases={len(documented)}")
print(f"boundary_nonempty_cases={len(boundaries)}")
print(f"exhaustive_cases={exhaustive_checked}")
print(f"deterministic_random_cases={random_checked}")
print(f"total_nonempty_cases={checked}")
print(f"mismatches_nonempty=0")
print(f"branch_relations={branch_relations}")
print(f"all_branch_boundaries_seen={all(v == {'LT', 'EQ', 'GT'} for v in branch_relations.values())}")
print(f"empty_canonical={empty_canonical}")
print(f"empty_candidate={empty_candidate}")
print("empty_domain_note=no non-empty subarray exists; both implementations reject the input")
