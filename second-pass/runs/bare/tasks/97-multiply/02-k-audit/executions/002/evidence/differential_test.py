#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test for 97-multiply."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


def decimal_unit_digit(value: int) -> int:
    """String-based oracle, independent of either implementation's arithmetic."""
    return int(str(value)[-1])


canonical = load_function(
    Path("/tmp/audit-work/reconstruction/canonical.py"), "trusted_canonical"
)
generated = load_function(
    Path("/tmp/audit-work/reconstruction/solution.py"), "generated_solution"
)

examples = [(148, 412), (19, 28), (2020, 1851), (14, -15)]
branch_boundaries = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]
digit_boundaries = [
    (a, b)
    for a in (-101, -100, -99, -11, -10, -9, 9, 10, 11, 99, 100, 101)
    for b in (-101, -100, -99, -11, -10, -9, 0, 9, 10, 11, 99, 100, 101)
]
large_boundaries = [
    (10**100, -(10**100 + 7)),
    (-(10**100 + 9), 10**100 + 8),
    (10**100 - 1, -(10**100 - 1)),
]

rng = random.Random(970097)
generated_inputs = [
    (
        rng.randint(-(10**100), 10**100),
        rng.randint(-(10**100), 10**100),
    )
    for _ in range(2000)
]

cases = examples + branch_boundaries + digit_boundaries + large_boundaries
cases += generated_inputs
encoded_inputs = json.dumps(cases, separators=(",", ":")).encode()
input_sha256 = hashlib.sha256(encoded_inputs).hexdigest()

canonical_generated_mismatches = []
canonical_string_oracle_mismatches = []
generated_string_oracle_mismatches = []
for a, b in cases:
    expected = decimal_unit_digit(a) * decimal_unit_digit(b)
    canonical_result = canonical(a, b)
    generated_result = generated(a, b)
    row = {
        "a": a,
        "b": b,
        "string_unit_digit_oracle": expected,
        "canonical": canonical_result,
        "generated": generated_result,
    }
    if canonical_result != generated_result:
        canonical_generated_mismatches.append(row)
    if canonical_result != expected:
        canonical_string_oracle_mismatches.append(row)
    if generated_result != expected:
        generated_string_oracle_mismatches.append(row)

print("ENTRY_POINT: multiply")
print("FORMAL_INPUT_KIND: pairs of Python integers")
print("EMPTY_CASE: not applicable to an integer-only input contract")
print(f"DOCUMENTED_EXAMPLES: {len(examples)}")
print(f"BRANCH_BOUNDARIES: {len(branch_boundaries)}")
print(f"DIGIT_BOUNDARY_CROSS_PRODUCT: {len(digit_boundaries)}")
print(f"LARGE_BOUNDARIES: {len(large_boundaries)}")
print(
    "GENERATED_INPUTS: 2000 pairs, seed=970097, "
    "each component uniform in [-10**100, 10**100]"
)
print(f"TOTAL_CASES: {len(cases)}")
print(f"INPUTS_JSON_SHA256: {input_sha256}")
print(
    "CANONICAL_VS_GENERATED_MISMATCHES: "
    f"{len(canonical_generated_mismatches)}"
)
print(
    "CANONICAL_VS_STRING_UNIT_DIGIT_MISMATCHES: "
    f"{len(canonical_string_oracle_mismatches)}"
)
print(
    "GENERATED_VS_STRING_UNIT_DIGIT_MISMATCHES: "
    f"{len(generated_string_oracle_mismatches)}"
)
if canonical_generated_mismatches:
    print("FIRST_CANONICAL_VS_GENERATED_MISMATCHES:")
    print(json.dumps(canonical_generated_mismatches[:20], indent=2))
    raise SystemExit(1)
print("DIFFERENTIAL_TEST: PASS")
