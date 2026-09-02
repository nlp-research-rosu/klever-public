#!/usr/bin/env python3
"""Independent candidate/canonical differential and contract-oracle test."""

import importlib.util
import math
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical_module = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate_module = load_module("candidate_solution", Path("/candidate/solution.py"))
canonical = canonical_module.intersection
candidate = candidate_module.intersection


def independent_is_prime(value: int) -> bool:
    if value < 2:
        return False
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def contract_oracle(interval1, interval2) -> str:
    length = min(interval1[1], interval2[1]) - max(interval1[0], interval2[0])
    return "YES" if independent_is_prime(length) else "NO"


named_cases = [
    ("prompt_example_touching", (1, 2), (2, 3), "NO"),
    ("prompt_example_length_one", (-1, 1), (0, 4), "NO"),
    ("prompt_example_length_two", (-3, -1), (-5, 5), "YES"),
    ("canonical_doc_example_length_five", (-3, 9), (-1, 4), "YES"),
    ("disjoint", (0, 1), (3, 4), "NO"),
    ("identical_empty_geometric_length", (5, 5), (5, 5), "NO"),
    ("equal_left_boundary", (0, 7), (0, 2), "YES"),
    ("second_left_less", (0, 7), (-4, 2), "YES"),
    ("second_left_greater", (-4, 7), (0, 2), "YES"),
    ("equal_right_boundary", (0, 2), (-4, 2), "YES"),
    ("second_right_greater", (0, 2), (-4, 7), "YES"),
    ("second_right_less", (0, 7), (-4, 2), "YES"),
    ("length_one_loop_not_entered", (0, 1), (0, 1), "NO"),
    ("length_two_loop_zero_iterations", (0, 2), (0, 2), "YES"),
    ("length_three_prime", (0, 3), (0, 3), "YES"),
    ("length_four_divisor_found", (0, 4), (0, 4), "NO"),
    ("length_six_multiple_divisors", (0, 6), (0, 6), "NO"),
    ("negative_coordinates_prime_length", (-101, -4), (-200, 100), "YES"),
    ("list_pair_inputs", [0, 13], [-20, 20], "YES"),
]

checked = 0
for name, interval1, interval2, expected in named_cases:
    oracle = contract_oracle(interval1, interval2)
    trusted = canonical(interval1, interval2)
    generated = candidate(interval1, interval2)
    assert oracle == expected, (name, "bad named expectation", oracle, expected)
    assert trusted == expected, (name, "canonical mismatch", trusted, expected)
    assert generated == expected, (name, "candidate mismatch", generated, expected)
    checked += 1

endpoints = range(-8, 9)
valid_intervals = [(start, end) for start in endpoints for end in endpoints if start <= end]
for interval1 in valid_intervals:
    for interval2 in valid_intervals:
        oracle = contract_oracle(interval1, interval2)
        trusted = canonical(interval1, interval2)
        generated = candidate(interval1, interval2)
        assert trusted == oracle, (interval1, interval2, trusted, oracle)
        assert generated == oracle, (interval1, interval2, generated, oracle)
        checked += 1

random_generator = random.Random(127)
for _ in range(2500):
    start1 = random_generator.randint(-500, 500)
    start2 = random_generator.randint(-500, 500)
    interval1 = (start1, start1 + random_generator.randint(0, 600))
    interval2 = (start2, start2 + random_generator.randint(0, 600))
    oracle = contract_oracle(interval1, interval2)
    trusted = canonical(interval1, interval2)
    generated = candidate(interval1, interval2)
    assert trusted == oracle, (interval1, interval2, trusted, oracle)
    assert generated == oracle, (interval1, interval2, generated, oracle)
    checked += 1

print(f"named_cases={len(named_cases)}")
print(f"exhaustive_endpoints=-8..8 valid_intervals={len(valid_intervals)} pairs={len(valid_intervals) ** 2}")
print("generated_cases=2500 seed=127 starts=-500..500 widths=0..600")
print(f"total_cases={checked}")
print("canonical_candidate_mismatches=0")
print("canonical_contract_oracle_mismatches=0")
print("candidate_contract_oracle_mismatches=0")
