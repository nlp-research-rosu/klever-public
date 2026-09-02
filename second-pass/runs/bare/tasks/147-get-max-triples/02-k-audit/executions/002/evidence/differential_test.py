#!/usr/bin/env python3
"""Independent differential test of trusted canonical versus candidate Python."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry("candidate_solution", Path("/candidate/solution.py"))


def direct_contract(n: int) -> int:
    values = [i * i - i + 1 for i in range(1, n + 1)]
    return sum(
        (values[i] + values[j] + values[k]) % 3 == 0
        for i in range(n)
        for j in range(i + 1, n)
        for k in range(j + 1, n)
    )


documented = {5: 1}
empty_and_small_boundaries = list(range(0, 13))
# This exhaustive interval crosses all three n mod 3 boundaries repeatedly,
# both sides of the first available triple, and both true/false divisibility
# branches in the trusted canonical's innermost conditional.
exhaustive = list(range(0, 81))
random.seed(147_20260726)
generated = sorted(set(random.randint(81, 180) for _ in range(30)))
canonical_inputs = sorted(set(empty_and_small_boundaries + exhaustive + generated))

mismatches = []
for n in canonical_inputs:
    trusted = canonical(n)
    generated_result = candidate(n)
    direct = direct_contract(n)
    if trusted != generated_result or trusted != direct:
        mismatches.append((n, trusted, generated_result, direct))

for n, expected in documented.items():
    assert canonical(n) == expected
    assert candidate(n) == expected


def residue_oracle(n: int) -> int:
    zeros = (n + 1) // 3
    ones = n - zeros
    return zeros * (zeros - 1) * (zeros - 2) // 6 + (
        ones * (ones - 1) * (ones - 2) // 6
    )


large_inputs = [181, 999, 10**6, 10**18, 10**30]
large_mismatches = [
    (n, candidate(n), residue_oracle(n))
    for n in large_inputs
    if candidate(n) != residue_oracle(n)
]

print("documented cases:", documented)
print("empty/small boundaries:", empty_and_small_boundaries)
print("canonical exhaustive interval: 0..80")
print("generated seed: 14720260726")
print("generated canonical inputs:", generated)
print("canonical comparison count:", len(canonical_inputs))
print("large residue-oracle inputs:", large_inputs)
print("canonical/candidate/direct mismatches:", mismatches)
print("candidate/residue-oracle large mismatches:", large_mismatches)
assert not mismatches
assert not large_mismatches
print("DIFFERENTIAL TEST: PASS")
