#!/usr/bin/env python3
"""Reviewer-authored differential for HumanEval 94."""

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.skjkasdkd


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical_94")
generated = load_function(Path("/candidate/solution.py"), "generated_solution_94")


def is_prime_math(n: int) -> bool:
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def docstring_oracle(values: list[int]) -> int:
    primes = [value for value in values if is_prime_math(value)]
    largest = max(primes, default=0)
    return sum(int(digit) for digit in str(largest))


examples = [
    ([0, 3, 2, 1, 3, 5, 7, 4, 5, 5, 5, 2, 181, 32, 4, 32, 3, 2, 32, 324, 4, 3], 10),
    ([1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1], 25),
    ([1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3], 13),
    ([0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6], 11),
    ([0, 81, 12, 3, 1, 21], 3),
    ([0, 8, 1, 2, 1, 7], 7),
]

directed = [
    [],
    [-5, -3, -1],
    [0],
    [1],
    [0, 1, 4, 6, 8, 9],
    [2],
    [3],
    [4],
    [2, 2],
    [3, 2, 3],
    [4, 5],
    [49, 47],
    [97, 89, 101, 100],
    [9973, 9972],
    [-7, 0, 1, 2, 25, 29, 29],
]

cases: list[tuple[str, list[int], int | None]] = [
    ("example", values, expected) for values, expected in examples
]
cases.extend(("directed", values, None) for values in directed)

boundary_values = [-5, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 19, 25, 49]
for length in range(5):
    cases.extend(
        ("exhaustive", list(values), None)
        for values in itertools.product(boundary_values, repeat=length)
    )

rng = random.Random(940730)
for _ in range(2000):
    cases.append(
        (
            "random",
            [rng.randint(-100, 500) for _ in range(rng.randint(0, 12))],
            None,
        )
    )

candidate_oracle_mismatches = []
canonical_candidate_mismatches = []
example_mismatches = []
category_counts: dict[str, int] = {}
for category, values, documented_expected in cases:
    category_counts[category] = category_counts.get(category, 0) + 1
    candidate_result = generated(values)
    canonical_result = canonical(values)
    oracle_result = docstring_oracle(values)
    if candidate_result != oracle_result:
        candidate_oracle_mismatches.append(
            (values, candidate_result, oracle_result)
        )
    if canonical_result != candidate_result:
        canonical_candidate_mismatches.append(
            (values, candidate_result, canonical_result, oracle_result)
        )
    if documented_expected is not None and candidate_result != documented_expected:
        example_mismatches.append(
            (values, candidate_result, documented_expected)
        )

print(f"category_counts={category_counts}")
print(f"total_cases={len(cases)}")
print(f"documented_example_mismatches={len(example_mismatches)}")
print(f"candidate_vs_docstring_oracle_mismatches={len(candidate_oracle_mismatches)}")
print(f"candidate_vs_canonical_mismatches={len(canonical_candidate_mismatches)}")
print("first_canonical_divergences=")
for mismatch in canonical_candidate_mismatches[:12]:
    print(mismatch)

assert not example_mismatches
assert not candidate_oracle_mismatches
assert all(
    oracle == candidate and candidate == 0
    and not any(is_prime_math(value) for value in values)
    and 1 in values
    for values, candidate, _canonical, oracle in canonical_candidate_mismatches
)
