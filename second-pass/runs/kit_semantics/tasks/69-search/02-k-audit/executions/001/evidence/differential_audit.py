#!/usr/bin/env python3
"""Independent differential audit for HumanEval 69-search."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from itertools import product
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_entry(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search


canonical_search = load_entry("trusted_canonical", SCRATCH / "canonical.py")
generated_search = load_entry("generated_solution", SCRATCH / "solution.py")


def contract_oracle(values: list[int]) -> int:
    qualifying = [
        value for value in set(values) if value > 0 and values.count(value) >= value
    ]
    return max(qualifying) if qualifying else -1


named_cases = {
    "documented_1": [4, 1, 2, 2, 3, 1],
    "documented_2": [1, 2, 2, 3, 3, 3, 4, 4, 4],
    "documented_3": [5, 5, 4, 4, 4],
    "minimum_equal": [1],
    "frequency_below": [2],
    "frequency_equal": [2, 2],
    "frequency_above": [2, 2, 2],
    "later_larger_update": [1, 2, 2],
    "later_smaller_no_update": [2, 2, 1],
    "two_equal_qualifiers_descending": [3, 3, 3, 2, 2],
    "two_equal_qualifiers_ascending": [2, 2, 3, 3, 3],
    "large_equal": [100] * 100,
    "large_below": [101] * 100,
    "large_value_and_length": [1000] * 1000,
}

cases: list[list[int]] = list(named_cases.values())
case_sources = {"named": len(cases)}

exhaustive = [
    list(values)
    for length in range(1, 8)
    for values in product(range(1, 7), repeat=length)
]
cases.extend(exhaustive)
case_sources["exhaustive_values_1_to_6_lengths_1_to_7"] = len(exhaustive)

threshold = []
for value in range(1, 51):
    for count in sorted({max(1, value - 1), value, value + 1}):
        threshold.append([value] * count)
        threshold.append(([1] if value != 1 else [2]) + [value] * count)
cases.extend(threshold)
case_sources["threshold_value_1_to_50_counts_v_minus_1_v_v_plus_1"] = len(threshold)

rng = random.Random(690729)
generated = []
for _ in range(2000):
    length = rng.randint(1, 100)
    generated.append([rng.randint(1, 150) for _ in range(length)])
cases.extend(generated)
case_sources["seeded_random_seed_690729"] = len(generated)

serialized = json.dumps(cases, separators=(",", ":")).encode()
print("intended_domain=non-empty finite lists of positive integers")
print("case_sources=" + json.dumps(case_sources, sort_keys=True))
print(f"case_count={len(cases)}")
print(f"case_corpus_sha256={hashlib.sha256(serialized).hexdigest()}")

mismatches = []
for index, values in enumerate(cases):
    expected = contract_oracle(values)
    canonical = canonical_search(values.copy())
    generated_result = generated_search(values.copy())
    if canonical != expected or generated_result != expected:
        mismatches.append(
            {
                "index": index,
                "input": values,
                "oracle": expected,
                "canonical": canonical,
                "generated": generated_result,
            }
        )

for name, values in named_cases.items():
    print(
        "named_result="
        + json.dumps(
            {
                "name": name,
                "input_length": len(values),
                "oracle": contract_oracle(values),
                "canonical": canonical_search(values.copy()),
                "generated": generated_search(values.copy()),
            },
            sort_keys=True,
        )
    )

def outcome(function, values):
    try:
        return {"return": function(values)}
    except Exception as err:  # boundary behavior is recorded, not hidden
        return {"exception": type(err).__name__, "message": str(err)}


print(
    "out_of_contract_empty="
    + json.dumps(
        {
            "canonical": outcome(canonical_search, []),
            "generated": outcome(generated_search, []),
        },
        sort_keys=True,
    )
)
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print("first_mismatches=" + json.dumps(mismatches[:10], sort_keys=True))
    raise SystemExit(1)
