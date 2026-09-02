#!/usr/bin/env python3
"""Independent differential checks for HumanEval 94.

The candidate and trusted canonical modules are loaded from their mounted/copy
paths.  `contract_oracle` is an independent iterative implementation of the
plain-language "largest prime, then digit sum" contract, with 0 when no prime
exists (the convention both implementations otherwise use via max=0).
"""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path
from typing import Callable


def load_entry(module_name: str, path: Path) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.skjkasdkd


def contract_oracle(values: list[int]) -> int:
    def prime(number: int) -> bool:
        if number < 2:
            return False
        for divisor in range(2, math.isqrt(number) + 1):
            if number % divisor == 0:
                return False
        return True

    best = max((value for value in values if prime(value)), default=0)
    return sum(int(digit) for digit in str(best))


def outcome(function: Callable[[list[int]], int], values: list[int]):
    try:
        return ("return", function(list(values)))
    except Exception as error:  # Deliberately compare observable exceptions.
        return ("raise", type(error).__name__, str(error))


candidate = load_entry(
    "audited_candidate_solution",
    Path("/tmp/audit-work/candidate-clean/solution.py"),
)
canonical = load_entry(
    "trusted_humaneval_canonical",
    Path("/reference/canonical.py"),
)

prompt_examples = [
    ([0, 3, 2, 1, 3, 5, 7, 4, 5, 5, 5, 2, 181, 32, 4, 32, 3, 2, 32, 324, 4, 3], 10),
    ([1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1], 25),
    ([1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3], 13),
    ([0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6], 11),
    ([0, 81, 12, 3, 1, 21], 3),
    ([0, 8, 1, 2, 1, 7], 7),
]

curated = [
    [],
    [-5],
    [0],
    [1],
    [1, 1],
    [-5, 1, 4],
    [4, 6, 8, 9],
    [2],
    [3],
    [4],
    [2, 3],
    [11, 7],
    [7, 7],
    [181],
    [997],
    [104729],
    [1000003],  # Exercises CPython recursion depth in the recursive rewrite.
]

small_values = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
exhaustive = [
    list(values)
    for length in range(4)
    for values in itertools.product(small_values, repeat=length)
]

generator = random.Random(940026)
random_cases = [
    [generator.randint(-100, 1000) for _ in range(generator.randint(0, 30))]
    for _ in range(1000)
]

cases = [values for values, _ in prompt_examples] + curated + exhaustive + random_cases
candidate_canonical_mismatches = []
candidate_contract_mismatches = []
canonical_contract_mismatches = []

for values in cases:
    generated_outcome = outcome(candidate, values)
    canonical_outcome = outcome(canonical, values)
    contract_outcome = outcome(contract_oracle, values)
    if generated_outcome != canonical_outcome:
        candidate_canonical_mismatches.append(
            (values, generated_outcome, canonical_outcome)
        )
    if generated_outcome != contract_outcome:
        candidate_contract_mismatches.append(
            (values, generated_outcome, contract_outcome)
        )
    if canonical_outcome != contract_outcome:
        canonical_contract_mismatches.append(
            (values, canonical_outcome, contract_outcome)
        )

example_failures = []
for values, expected in prompt_examples:
    generated_outcome = outcome(candidate, values)
    canonical_outcome = outcome(canonical, values)
    if generated_outcome != ("return", expected) or canonical_outcome != (
        "return",
        expected,
    ):
        example_failures.append(
            (values, expected, generated_outcome, canonical_outcome)
        )

print(f"prompt_examples={len(prompt_examples)} failures={len(example_failures)}")
print(f"curated_cases={len(curated)}")
print(f"exhaustive_cases={len(exhaustive)} lengths=0..3 values={small_values}")
print("random_cases=1000 seed=940026 lengths=0..30 values=-100..1000")
print(f"total_cases={len(cases)}")
print(
    "candidate_vs_canonical_mismatches="
    f"{len(candidate_canonical_mismatches)}"
)
print(
    "candidate_vs_contract_mismatches="
    f"{len(candidate_contract_mismatches)}"
)
print(
    "canonical_vs_contract_mismatches="
    f"{len(canonical_contract_mismatches)}"
)
print(f"example_failures={example_failures}")
print(
    "first_candidate_canonical_mismatches="
    f"{candidate_canonical_mismatches[:20]}"
)
print(
    "first_candidate_contract_mismatches="
    f"{candidate_contract_mismatches[:20]}"
)
print(
    "first_canonical_contract_mismatches="
    f"{canonical_contract_mismatches[:20]}"
)
