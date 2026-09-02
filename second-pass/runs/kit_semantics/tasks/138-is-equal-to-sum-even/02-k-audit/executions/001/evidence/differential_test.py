#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    specification = importlib.util.spec_from_file_location(module_name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module.is_equal_to_sum_even


canonical = load_entry(
    Path("/tmp/audit-work/138-audit/reference/canonical.py"), "trusted_canonical"
)
candidate = load_entry(
    Path("/tmp/audit-work/138-audit/candidate/solution.py"), "candidate_solution"
)

documented_examples = [4, 6, 8]
branch_boundaries = [
    -10,
    -9,
    -2,
    -1,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
]
huge_boundaries = [
    -(10**100),
    -(10**100) + 1,
    10**100,
    10**100 + 1,
]
exhaustive_small = list(range(-200, 201))
generator = random.Random(138)
generated = [generator.randint(-(10**30), 10**30) for _ in range(256)]
inputs = list(
    dict.fromkeys(
        documented_examples
        + branch_boundaries
        + huge_boundaries
        + exhaustive_small
        + generated
    )
)

mismatches = []
oracle_mismatches = []
for value in inputs:
    expected = canonical(value)
    actual = candidate(value)
    contract_oracle = value >= 8 and value % 2 == 0
    if expected != actual:
        mismatches.append((value, expected, actual))
    if expected != contract_oracle or actual != contract_oracle:
        oracle_mismatches.append((value, expected, actual, contract_oracle))

outside_domain = [False, True, -2.0, 7.5, 8.0, 9.0, None]
outside_observations = []
for value in outside_domain:
    row = [repr(value)]
    for function in (canonical, candidate):
        try:
            row.append(("value", function(value)))
        except Exception as error:  # Diagnostic only: these are not K Int inputs.
            row.append(("exception", type(error).__name__))
    outside_observations.append(tuple(row))

print(f"documented_examples={documented_examples}")
print(f"branch_boundaries={branch_boundaries}")
print(f"huge_boundaries={huge_boundaries}")
print("exhaustive_small=range(-200,201)")
print("generated_seed=138 generated_count=256 generated_bounds=[-10**30,10**30]")
print(f"all_int_inputs={inputs}")
print(f"int_cases={len(inputs)} canonical_candidate_mismatches={len(mismatches)}")
print(f"contract_oracle_mismatches={len(oracle_mismatches)}")
print(f"outside_domain_observations={outside_observations}")
if mismatches or oracle_mismatches:
    print(f"mismatches={mismatches}")
    print(f"oracle_mismatches={oracle_mismatches}")
    raise SystemExit(1)
print("DIFFERENTIAL_TEST=PASS")
