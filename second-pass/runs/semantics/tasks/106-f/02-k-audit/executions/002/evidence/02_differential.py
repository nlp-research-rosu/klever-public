#!/usr/bin/env python3
"""Independent differential and contract-oracle checks for HumanEval/106."""

import hashlib
import importlib.util
import json
import math
import random
from pathlib import Path


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


def contract_oracle(n: int):
    return [
        math.factorial(i) if i % 2 == 0 else i * (i + 1) // 2
        for i in range(1, n + 1)
    ]


canonical = load_entry("/reference/canonical.py", "trusted_canonical_106")
generated = load_entry("/tmp/audit-work/reconstruction/solution.py", "generated_106")

# 0 is the empty-list boundary; 1 and 2 enter the odd/even branches; 3 and 4
# cover both transitions; 5 is the documented example. Negative cases record
# implementation behavior outside the meaningful nonnegative "list size n"
# contract. The seeded sample broadens coverage without hiding the inputs.
documented_and_boundaries = [-5, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 50]
rng = random.Random(106)
generated_inputs = [rng.randrange(0, 81) for _ in range(200)]
inputs = documented_and_boundaries + generated_inputs

mismatches = []
records = []
for n in inputs:
    trusted = canonical(n)
    actual = generated(n)
    oracle = contract_oracle(n)
    ok = trusted == actual == oracle
    if not ok:
        mismatches.append(
            {"n": n, "canonical": trusted, "generated": actual, "oracle": oracle}
        )
    encoded = json.dumps(actual, separators=(",", ":")).encode()
    records.append(
        {
            "n": n,
            "length": len(actual),
            "sha256": hashlib.sha256(encoded).hexdigest(),
            "ok": ok,
        }
    )

print("documented_and_boundary_inputs =", documented_and_boundaries)
print("random_seed = 106")
print("generated_inputs =", generated_inputs)
print("case_count =", len(inputs))
print("mismatch_count =", len(mismatches))
print("mismatches =", json.dumps(mismatches, sort_keys=True))
print("per_case_results =", json.dumps(records, sort_keys=True))

assert canonical(5) == generated(5) == [1, 2, 6, 24, 15]
assert not mismatches
