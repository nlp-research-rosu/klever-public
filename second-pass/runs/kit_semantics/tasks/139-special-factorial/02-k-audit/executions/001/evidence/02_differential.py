#!/usr/bin/env python3
"""Independent program-fidelity comparison for HumanEval 139."""

import importlib.util
import math
import pathlib
import random
import sys


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


trusted = load_module("trusted_canonical_139", pathlib.Path("/reference/canonical.py"))
generated = load_module(
    "generated_solution_139",
    pathlib.Path("/tmp/audit-work/reconstruction/solution.py"),
)

# The first block covers the out-of-domain no-iteration behavior, the positive
# boundary, the stated example, and the first several distinct loop lengths.
fixed_inputs = [-3, -1, 0, 1, 2, 3, 4, 5, 6, 7, 10, 20, 50]
rng = random.Random(139)
generated_inputs = sorted({rng.randint(1, 75) for _ in range(40)})
inputs = fixed_inputs + [n for n in generated_inputs if n not in fixed_inputs]

mismatches = []
for n in inputs:
    canonical_value = trusted.special_factorial(n)
    generated_value = generated.special_factorial(n)
    contract_value = math.prod(math.factorial(k) for k in range(1, n + 1))
    if generated_value != canonical_value:
        mismatches.append((n, "candidate-vs-canonical", generated_value, canonical_value))
    if n > 0 and generated_value != contract_value:
        mismatches.append((n, "candidate-vs-independent-contract", generated_value, contract_value))

print(f"fixed_inputs={fixed_inputs}")
print(f"generated_seed=139 generated_inputs={generated_inputs}")
print(f"total_inputs={len(inputs)}")
print(f"documented_example_n4={generated.special_factorial(4)}")
print(
    "positive_boundaries="
    f"n1:{generated.special_factorial(1)},"
    f"n2:{generated.special_factorial(2)}"
)
print(
    "out_of_domain_no_iteration="
    f"n-1:{generated.special_factorial(-1)},"
    f"n0:{generated.special_factorial(0)}"
)
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", mismatch)

sys.exit(1 if mismatches else 0)
