#!/usr/bin/env python3
"""Independent differential test for HumanEval 59.

The oracle and candidate are imported from separate, explicit source paths.
The intended domain is composite integers greater than one. Scalar input has
no meaningful "empty" case, so 0 and 1 are included only as out-of-contract
robustness observations.
"""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


oracle_module = load_module(
    "trusted_canonical", Path("/tmp/audit-work/review-59/trusted/canonical.py")
)
candidate_module = load_module(
    "scratch_solution", Path("/tmp/audit-work/review-59/candidate-src/solution.py")
)
oracle = oracle_module.largest_prime_factor
candidate = candidate_module.largest_prime_factor


def is_composite(n: int) -> bool:
    return n > 1 and any(n % divisor == 0 for divisor in range(2, n))


documented = [13195, 2048]
branch_and_boundary = [4, 6, 8, 9, 12, 15, 25, 49]
exhaustive = [n for n in range(4, 501) if is_composite(n)]
rng = random.Random(590059)
generated = sorted({rng.randint(2, 100) * rng.randint(2, 100) for _ in range(150)})
intended_inputs = list(
    dict.fromkeys(documented + branch_and_boundary + exhaustive + generated)
)
out_of_contract = [0, 1, 2, 3, 5, 7]

print("intended_inputs=" + json.dumps(intended_inputs, separators=(",", ":")))
print("out_of_contract_inputs=" + json.dumps(out_of_contract))

intended_mismatches = []
for n in intended_inputs:
    expected = oracle(n)
    actual = candidate(n)
    if expected != actual:
        intended_mismatches.append({"n": n, "canonical": expected, "candidate": actual})

out_of_contract_observations = []
for n in out_of_contract:
    expected = oracle(n)
    actual = candidate(n)
    out_of_contract_observations.append(
        {"n": n, "canonical": expected, "candidate": actual}
    )

examples = {
    str(n): {"canonical": oracle(n), "candidate": candidate(n)}
    for n in documented + branch_and_boundary
}
print("examples=" + json.dumps(examples, sort_keys=True))
print(
    "out_of_contract_observations="
    + json.dumps(out_of_contract_observations, sort_keys=True)
)
print(f"intended_count={len(intended_inputs)}")
print(f"intended_mismatch_count={len(intended_mismatches)}")
print("intended_mismatches=" + json.dumps(intended_mismatches, sort_keys=True))

if intended_mismatches:
    raise SystemExit(1)
