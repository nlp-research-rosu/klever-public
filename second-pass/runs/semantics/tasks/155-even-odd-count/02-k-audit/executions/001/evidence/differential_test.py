#!/usr/bin/env python3
"""Independent differential check for HumanEval 155 on the integer domain."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_count


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
generated = load_entry(
    "candidate_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

# The integer domain has no value whose abs-value has an empty decimal
# representation. Zero is the unique minimal one-character boundary case.
documented = [-12, 123]
boundaries = [
    0,
    -1,
    1,
    -2,
    2,
    -9,
    9,
    -10,
    10,
    -11,
    11,
    -12,
    12,
    -19,
    19,
    -20,
    20,
    -99,
    99,
    -100,
    100,
    -101,
    101,
    -102,
    102,
    -24680,
    24680,
    -13579,
    13579,
    102030405,
    10**50,
    -(10**50),
    int("20" * 50),
    -int("13579" * 20),
]
exhaustive_small = list(range(-10_000, 10_001))

rng = random.Random(155)
generated_inputs = []
for _ in range(2_000):
    bit_count = rng.randint(0, 512)
    value = rng.getrandbits(bit_count)
    if rng.randrange(2):
        value = -value
    generated_inputs.append(value)

inputs = list(
    dict.fromkeys(documented + boundaries + exhaustive_small + generated_inputs)
)
Path("/audit-output/evidence/differential_inputs.json").write_text(
    json.dumps(inputs, indent=2) + "\n", encoding="utf-8"
)

mismatches = []
seen_digits = set()
for number in inputs:
    seen_digits.update(str(abs(number)))
    expected = canonical(number)
    actual = generated(number)
    if expected != actual or type(expected) is not type(actual):
        mismatches.append(
            {
                "input": number,
                "canonical": repr(expected),
                "generated": repr(actual),
                "canonical_type": type(expected).__name__,
                "generated_type": type(actual).__name__,
            }
        )

summary = {
    "oracle": "/tmp/audit-work/trusted/canonical.py:even_odd_count",
    "implementation": "/tmp/audit-work/candidate-src/solution.py:even_odd_count",
    "documented_examples": documented,
    "empty_case": "not realizable for an integer; zero is the minimal decimal representation",
    "input_count": len(inputs),
    "exhaustive_interval": [-10_000, 10_000],
    "deterministic_random_seed": 155,
    "deterministic_random_count": len(generated_inputs),
    "random_bit_width_range": [0, 512],
    "decimal_digits_seen": sorted(seen_digits),
    "mismatch_count": len(mismatches),
    "first_mismatches": mismatches[:20],
}
print(json.dumps(summary, indent=2))

if sorted(seen_digits) != list("0123456789"):
    raise AssertionError("branch-driving decimal digits 0 through 9 were not all covered")
if mismatches:
    raise AssertionError(f"{len(mismatches)} differential mismatch(es)")
