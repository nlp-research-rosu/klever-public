#!/usr/bin/env python3
"""Independent differential check of trusted canonical vs submitted solution."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_152", "/reference/canonical.py").compare
generated = load(
    "submitted_generated_152", "/tmp/audit-work/152-compare/solution.py"
).compare


fixed_cases = [
    # Documented examples.
    ([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]),
    ([0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]),
    # Empty branch and single-element branch boundaries: d < 0, d == 0, d > 0.
    ([], []),
    ([0], [1]),
    ([0], [0]),
    ([1], [0]),
    ([-1], [0]),
    ([0], [-1]),
    # Integer magnitude/sign boundaries relevant to subtraction and negation.
    ([-10**100, 10**100], [10**100, -(10**100)]),
    ([-(2**63), 2**63 - 1], [2**63 - 1, -(2**63)]),
]

rng = random.Random(152)
random_cases = []
for length in list(range(0, 33)) + [50, 100, 250, 500, 900]:
    for _ in range(5):
        game = [rng.randint(-(10**30), 10**30) for _ in range(length)]
        guess = [rng.randint(-(10**30), 10**30) for _ in range(length)]
        random_cases.append((game, guess))

cases = fixed_cases + random_cases
mismatches = []
serialized_inputs = []
for index, (game, guess) in enumerate(cases):
    expected = canonical(game, guess)
    actual = generated(game, guess)
    serialized_inputs.append([game, guess])
    if actual != expected:
        mismatches.append(
            {"index": index, "game": game, "guess": guess, "expected": expected, "actual": actual}
        )

input_digest = hashlib.sha256(
    json.dumps(serialized_inputs, separators=(",", ":")).encode()
).hexdigest()
print(f"ordinary_case_count={len(cases)}")
print(f"ordinary_input_sha256={input_digest}")
print(f"ordinary_mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(json.dumps(mismatch, sort_keys=True))

# Record the real-CPython recursion/resource boundary separately. This is not a
# value mismatch when the submitted function returns; it identifies where the
# recursive implementation raises while the list-comprehension oracle returns.
resource_cases = [950, 975, 990, 995, 999, 1000, 1050, 1100]
resource_divergences = []
for length in resource_cases:
    game = list(range(length))
    guess = list(reversed(game))
    expected = canonical(game, guess)
    try:
        actual = generated(game, guess)
        generated_status = f"returned:{len(actual)}"
        equal = actual == expected
    except Exception as err:
        generated_status = f"raised:{type(err).__name__}:{err}"
        equal = False
    print(
        f"resource_length={length} canonical=returned:{len(expected)} "
        f"generated={generated_status} equal={equal}"
    )
    if not equal:
        resource_divergences.append((length, generated_status))

print(f"resource_divergence_count={len(resource_divergences)}")

if mismatches:
    raise SystemExit(1)
