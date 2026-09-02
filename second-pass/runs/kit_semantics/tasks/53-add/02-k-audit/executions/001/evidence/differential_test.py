#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/53."""

from __future__ import annotations

import importlib.util
import operator
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


canonical_add = load_entry("trusted_canonical_53", Path("/reference/canonical.py"))
candidate_add = load_entry(
    "scratch_candidate_53", Path("/tmp/audit-work/reconstruction/solution.py")
)

# The first two are the documented examples. The rest cover zero, signs,
# cancellation, small integer boundaries, common machine-word boundaries, and
# very large CPython integers. Addition has no control-flow branch boundary and
# no meaningful "empty" input for its two required integer arguments.
fixed_cases = [
    (2, 3),
    (5, 7),
    (0, 0),
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, -1),
    (-1, 1),
    (-1, -1),
    (2**31 - 1, 1),
    (-(2**31), -1),
    (2**63 - 1, 1),
    (-(2**63), -1),
    (10**100, -(10**100)),
    (10**100, 10**100),
    (-(10**100), -(10**100)),
]

rng = random.Random(530053)
generated_cases = [
    (
        rng.randint(-(10**80), 10**80),
        rng.randint(-(10**80), 10**80),
    )
    for _ in range(200)
]

cases = fixed_cases + generated_cases
mismatches = []
for index, (x, y) in enumerate(cases):
    trusted = canonical_add(x, y)
    generated = candidate_add(x, y)
    independent = operator.add(x, y)
    if trusted != generated or trusted != independent:
        mismatches.append(
            {
                "index": index,
                "x": x,
                "y": y,
                "trusted": trusted,
                "generated": generated,
                "operator": independent,
            }
        )
    print(f"CASE {index:03d} x={x} y={y}")

print("EMPTY_CASES: not applicable to a two-required-integer-argument contract")
print("CONTROL_FLOW_BRANCH_BOUNDARIES: none in either implementation")
print(f"FIXED_CASES={len(fixed_cases)}")
print("GENERATED_SEED=530053")
print(f"GENERATED_CASES={len(generated_cases)}")
print(f"TOTAL_CASES={len(cases)}")
print(f"MISMATCHES={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch}")

raise SystemExit(1 if mismatches else 0)
