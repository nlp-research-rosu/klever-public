#!/usr/bin/env python3
"""Independent differential test for HumanEval/159 over its documented domain."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/159-eat-audit")
INPUT_RECORD = Path("/audit-output/evidence/differential_inputs.json")


def import_from(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = import_from(ROOT / "trusted/canonical.py", "trusted_canonical")
generated = import_from(ROOT / "rebuild/solution.py", "candidate_solution")


def independent_contract(number: int, need: int, remaining: int) -> list[int]:
    eaten = min(need, remaining)
    return [number + eaten, remaining - eaten]


cases: set[tuple[int, int, int]] = set()
examples = {
    (5, 6, 10),
    (4, 8, 9),
    (1, 10, 10),
    (2, 11, 5),
}
cases.update(examples)

# Empty/minimum/maximum and representative Cartesian boundaries.
values = (0, 1, 2, 10, 499, 500, 999, 1000)
for number in values:
    for need in values:
        for remaining in values:
            cases.add((number, need, remaining))

# Exhaust a dense small cube.
for number in range(21):
    for need in range(21):
        for remaining in range(21):
            cases.add((number, need, remaining))

# Exercise both sides of every need-vs-remaining branch boundary for each stock
# value, at low and high values of the already-eaten parameter.
for number in (0, 1, 999, 1000):
    for remaining in range(1001):
        for need in (remaining - 1, remaining, remaining + 1):
            if 0 <= need <= 1000:
                cases.add((number, need, remaining))

# Deterministic representative generated inputs across the entire domain.
rng = random.Random(159_20260726)
for _ in range(10_000):
    cases.add(
        (
            rng.randrange(1001),
            rng.randrange(1001),
            rng.randrange(1001),
        )
    )

ordered_cases = sorted(cases)
serialized = json.dumps(ordered_cases, separators=(",", ":"))
INPUT_RECORD.write_text(serialized + "\n", encoding="utf-8")

mismatches: list[dict[str, object]] = []
branch_counts = {"need<=remaining": 0, "need>remaining": 0}
for number, need, remaining in ordered_cases:
    branch_counts[
        "need<=remaining" if need <= remaining else "need>remaining"
    ] += 1
    expected = canonical.eat(number, need, remaining)
    observed = generated.eat(number, need, remaining)
    contract = independent_contract(number, need, remaining)
    if expected != observed or expected != contract:
        mismatches.append(
            {
                "input": [number, need, remaining],
                "canonical": expected,
                "generated": observed,
                "independent_contract": contract,
            }
        )
        if len(mismatches) >= 20:
            break

input_sha256 = hashlib.sha256((serialized + "\n").encode()).hexdigest()
print(f"python={sys.version.split()[0]}")
print(f"cases={len(ordered_cases)}")
print(f"examples={len(examples)}")
print(f"branch_counts={branch_counts}")
print(f"input_record={INPUT_RECORD}")
print(f"input_sha256={input_sha256}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches, indent=2, sort_keys=True))
    sys.exit(1)
print("RESULT differential equivalence and independent contract checks passed")
