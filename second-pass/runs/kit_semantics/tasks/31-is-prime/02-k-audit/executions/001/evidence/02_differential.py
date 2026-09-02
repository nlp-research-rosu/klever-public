#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test for HumanEval/31."""

import importlib.util
import json
import math
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime


def independent_oracle(n: int) -> bool:
    if n < 2:
        return False
    return all(n % divisor != 0 for divisor in range(2, math.isqrt(n) + 1))


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "scratch_generated", Path("/tmp/audit-work/prime31/solution.py")
)

# The input is a scalar integer, so there is no valid "empty collection" case.
# This set includes every source control boundary, every documented example,
# exhaustive small integers, late/early composites, and deterministic samples.
documented = [6, 101, 11, 13441, 61, 4, 1]
branch_boundaries = [
    -10**6,
    -2,
    -1,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    8,
    9,
    15,
    25,
    49,
    97,
    121,
    997,
    999,
    1000,
    1009,
    9991,
    10000,
]
rng = random.Random(31031)
generated_inputs = [rng.randint(-500, 3000) for _ in range(200)]
inputs = sorted(set(range(-50, 601)) | set(documented) | set(branch_boundaries) | set(generated_inputs))

mismatches = []
for n in inputs:
    c_value = canonical(n)
    g_value = generated(n)
    o_value = independent_oracle(n)
    if not (c_value == g_value == o_value):
        mismatches.append(
            {
                "input": n,
                "canonical": c_value,
                "generated": g_value,
                "oracle": o_value,
            }
        )

print("contract_domain=integer")
print("empty_case=not_applicable_scalar_input")
print(f"input_count={len(inputs)}")
print("inputs_json=" + json.dumps(inputs, separators=(",", ":")))
print("documented_examples_json=" + json.dumps(documented, separators=(",", ":")))
print("mismatches_json=" + json.dumps(mismatches, separators=(",", ":")))
if mismatches:
    raise SystemExit(1)
print("RESULT=PASS")
