#!/usr/bin/env python3
"""Independent differential test for HumanEval/123-get-odd-collatz."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import random
from pathlib import Path
from typing import Callable


def load_entry(module_name: str, path: Path) -> Callable[[int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_odd_collatz


def contract_oracle(n: int) -> list[int]:
    """Direct exact-integer implementation of the natural-language contract."""
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("contract domain is positive integers")
    odd_values: list[int] = []
    current = n
    while True:
        if current % 2 == 1:
            odd_values.append(current)
        if current == 1:
            return sorted(odd_values)
        current = current // 2 if current % 2 == 0 else 3 * current + 1


canonical = load_entry("trusted_humaneval_123_canonical", Path("/reference/canonical.py"))
generated = load_entry("candidate_humaneval_123_solution", Path("/candidate/solution.py"))

documented_and_boundaries = [1, 5, 2, 3, 4, 6, 7, 8, 9, 27]
randomizer = random.Random(123_20260726)
generated_inputs = [randomizer.randint(1, 50_000) for _ in range(300)]
numeric_representation_boundaries = [
    2**31 - 1,
    2**31,
    2**31 + 1,
    2**53 - 1,
    2**53,
    2**53 + 1,
    2**53 + 2,
    2**54 + 1,
    2**55 + 3,
]
inputs = list(
    dict.fromkeys(
        documented_and_boundaries + generated_inputs + numeric_representation_boundaries
    )
)

canonical_mismatches: list[tuple[int, list[int], list[int]]] = []
generated_mismatches: list[tuple[int, list[int], list[int]]] = []
direct_mismatches: list[tuple[int, list[int], list[int]]] = []

for n in inputs:
    expected = contract_oracle(n)
    canonical_result = canonical(n)
    generated_result = generated(n)
    if canonical_result != expected:
        canonical_mismatches.append((n, canonical_result, expected))
    if generated_result != expected:
        generated_mismatches.append((n, generated_result, expected))
    if generated_result != canonical_result:
        direct_mismatches.append((n, generated_result, canonical_result))

print("CONTRACT_DOMAIN: positive integers")
print("EMPTY_CASE: not applicable; the input is a scalar positive integer")
print("OUT_OF_DOMAIN_ZERO: intentionally not invoked; neither contract nor partial correctness requires it")
print(f"TOTAL_DISTINCT_INPUTS: {len(inputs)}")
print(f"DOCUMENTED_AND_BRANCH_BOUNDARIES: {documented_and_boundaries}")
print(f"RANDOM_SEED: 12320260726")
print("RANDOM_RANGE: 300 draws uniformly from [1, 50000]")
print(f"NUMERIC_REPRESENTATION_BOUNDARIES: {numeric_representation_boundaries}")
print(f"CANONICAL_VS_CONTRACT_MISMATCHES: {len(canonical_mismatches)}")
print(f"GENERATED_VS_CONTRACT_MISMATCHES: {len(generated_mismatches)}")
print(f"GENERATED_VS_CANONICAL_MISMATCHES: {len(direct_mismatches)}")

for label, mismatches in (
    ("CANONICAL_VS_CONTRACT", canonical_mismatches),
    ("GENERATED_VS_CONTRACT", generated_mismatches),
    ("GENERATED_VS_CANONICAL", direct_mismatches),
):
    for n, actual, expected in mismatches:
        actual_digest = hashlib.sha256(json.dumps(actual).encode()).hexdigest()[:16]
        expected_digest = hashlib.sha256(json.dumps(expected).encode()).hexdigest()[:16]
        print(
            f"{label}: n={n} actual_len={len(actual)} expected_len={len(expected)} "
            f"actual_sha256_16={actual_digest} expected_sha256_16={expected_digest} "
            f"actual_prefix={actual[:12]} expected_prefix={expected[:12]}"
        )

assert not generated_mismatches, "candidate diverges from exact-integer contract oracle"
