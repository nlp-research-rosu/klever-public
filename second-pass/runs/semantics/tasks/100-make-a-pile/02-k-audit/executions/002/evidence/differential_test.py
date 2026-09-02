#!/usr/bin/env python3
"""Independent differential check for HumanEval/100."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_a_pile


canonical = load_entry("trusted_canonical_100", Path("/reference/canonical.py"))
candidate = load_entry("candidate_solution_100", Path("/candidate/solution.py"))

# n=1 is the smallest contract input and takes one true loop guard followed by
# one false loop guard. n=2 covers even parity; n=3 is the documented example.
# 1..256 exhaustively covers small positive values and both parities.
rng = random.Random(100_20260726)
positive_inputs = list(range(1, 257))
positive_inputs += [257, 511, 512, 999, 1000, 4096]
positive_inputs += [rng.randint(1, 10_000) for _ in range(64)]
positive_inputs = sorted(set(positive_inputs))

mismatches = []
for n in positive_inputs:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected:
        mismatches.append((n, expected, actual))
    assert len(actual) == n
    assert actual[0] == n
    assert actual[-1] == n + 2 * (n - 1)
    assert all(actual[index] == n + 2 * index for index in range(n))

# These values are explicitly outside the "positive integer" contract. They
# are diagnostic empty/below-boundary checks, not claimed theorem coverage.
outside_domain_inputs = [-5, -1, 0]
outside_results = [
    (n, canonical(n), candidate(n))
    for n in outside_domain_inputs
]

print(f"positive_input_count={len(positive_inputs)}")
print(f"positive_inputs={positive_inputs}")
print("documented_example n=3 result=", candidate(3))
print("minimum_positive n=1 result=", candidate(1))
print("first_even n=2 result=", candidate(2))
print(f"outside_domain_results={outside_results}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(f"mismatches={mismatches}")
    raise SystemExit(1)
print("DIFFERENTIAL_OK")
