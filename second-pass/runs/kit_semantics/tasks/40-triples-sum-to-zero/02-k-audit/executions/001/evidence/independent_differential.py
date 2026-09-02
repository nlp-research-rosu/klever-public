#!/usr/bin/env python3
"""Independent candidate/canonical/specification differential check."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


candidate = load_function("/candidate/solution.py", "audited_candidate_solution")
canonical = load_function("/reference/canonical.py", "trusted_canonical_solution")


def contract_oracle(values: list[int]) -> bool:
    return any(a + b + c == 0 for a, b, c in itertools.combinations(values, 3))


documented_and_boundaries = [
    [1, 3, 5, 0],
    [1, 3, -2, 1],
    [1, 2, 3, 7],
    [2, 4, -5, 3, 9, 7],
    [1],
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [1, -1, 0],
    [1, -1, 2],
    [5, 5, -10],
    [5, -10, 5],
    [-10, 5, 5],
    [1, 1, 1],
    [10**100, -(10**100), 0],
    [10**100, 10**100, -(2 * 10**100)],
    [10**100, 1, -(10**100), 9],
]

rng = random.Random(40)
random_cases = [
    [rng.randint(-10**30, 10**30) for _ in range(rng.randint(0, 15))]
    for _ in range(1000)
]
exhaustive_cases = (
    list(values)
    for length in range(6)
    for values in itertools.product(range(-3, 4), repeat=length)
)

checked = 0
mismatches: list[dict[str, object]] = []
corpus_hasher = hashlib.sha256()
true_count = 0
false_count = 0
for values in itertools.chain(
    documented_and_boundaries, exhaustive_cases, random_cases
):
    expected = contract_oracle(values)
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    corpus_hasher.update(json.dumps(values, separators=(",", ":")).encode() + b"\n")
    checked += 1
    true_count += int(expected)
    false_count += int(not expected)
    if (
        type(canonical_result) is not bool
        or type(candidate_result) is not bool
        or canonical_result != expected
        or candidate_result != expected
    ):
        mismatches.append(
            {
                "values": values,
                "oracle": expected,
                "canonical": canonical_result,
                "candidate": candidate_result,
            }
        )
        if len(mismatches) <= 10:
            print("MISMATCH", mismatches[-1])

print("FIXED_CASES=18")
print("EXHAUSTIVE_SCOPE=lengths 0..5, values -3..3")
print("EXHAUSTIVE_CASES=19608")
print("RANDOM_SCOPE=seed 40, 1000 lists, lengths 0..15, values ±10^30")
print(f"TOTAL_CASES={checked}")
print(f"TRUE_CASES={true_count}")
print(f"FALSE_CASES={false_count}")
print(f"CORPUS_SHA256={corpus_hasher.hexdigest()}")
print(f"MISMATCHES={len(mismatches)}")
assert checked == 18 + 19608 + 1000
assert not mismatches
