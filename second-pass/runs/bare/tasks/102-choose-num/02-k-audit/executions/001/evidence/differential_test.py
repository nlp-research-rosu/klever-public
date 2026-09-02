#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 102."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def direct_contract_oracle(x: int, y: int) -> int:
    """Search only the at-most-two possible maximal endpoints."""
    if x > y:
        return -1
    if y % 2 == 0:
        return y
    if y - 1 >= x:
        return y - 1
    return -1


canonical = load_module("trusted_humaneval_102", Path("/reference/canonical.py"))
generated = load_module("generated_solution_102", Path("/tmp/audit-work/solution.py"))

documented = [(12, 15), (13, 12)]
branch_boundaries = [
    (1, 1),      # smallest positive odd singleton
    (2, 2),      # smallest positive even singleton
    (1, 2),      # x < y, y even
    (2, 1),      # first empty/reversed interval
    (2, 3),      # x < y, y odd
    (3, 3),      # x == y, y odd
    (3, 4),      # transition from odd singleton to even endpoint
    (4, 5),      # adjacent endpoints, odd y
    (999_999, 1_000_000),
    (1_000_000, 999_999),
]
exhaustive_small = [(x, y) for x in range(1, 101) for y in range(1, 101)]
rng = random.Random(102_20260723)
generated_inputs = [
    (rng.randint(1, 10**12), rng.randint(1, 10**12))
    for _ in range(1000)
]

cases = []
seen = set()
for pair in documented + branch_boundaries + exhaustive_small + generated_inputs:
    if pair not in seen:
        seen.add(pair)
        cases.append(pair)

input_path = Path("/audit-output/evidence/differential-inputs.json")
input_path.write_text(json.dumps(cases, separators=(",", ":")) + "\n", encoding="utf-8")
input_digest = hashlib.sha256(input_path.read_bytes()).hexdigest()

mismatches = []
for x, y in cases:
    expected = direct_contract_oracle(x, y)
    trusted = canonical.choose_num(x, y)
    actual = generated.choose_num(x, y)
    if trusted != expected or actual != trusted:
        mismatches.append(
            {
                "x": x,
                "y": y,
                "contract": expected,
                "canonical": trusted,
                "generated": actual,
            }
        )

print(f"documented_count={len(documented)} values={documented}")
print(f"branch_boundary_count={len(branch_boundaries)} values={branch_boundaries}")
print("exhaustive_small_domain=x,y in [1,100]")
print("generated_seed=10220260723 generated_count=1000 range=[1,10^12]")
print(f"unique_case_count={len(cases)}")
print(f"input_file={input_path}")
print(f"input_sha256={input_digest}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], indent=2))
    raise SystemExit(1)
print("RESULT: all generated outputs equal the trusted canonical and direct contract oracle")
