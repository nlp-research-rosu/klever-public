#!/usr/bin/env python3
"""Independent program-fidelity test for HumanEval 84.

The trusted canonical implementation is the oracle.  The candidate module is
loaded from a different path and no candidate helper or proof equation is
reused.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_humaneval_84", Path("/reference/canonical.py"))
candidate = load_module("candidate_humaneval_84", Path("/candidate/solution.py"))

documented = {1000: "1", 150: "110", 147: "1100"}
for value, expected in documented.items():
    assert canonical.solve(value) == expected
    assert candidate.solve(value) == expected

# There is no "empty" value in the declared integer domain.  Zero is the
# lower boundary and is included explicitly.  Adjacent values exercise every
# decimal-place boundary used by the candidate expression.
branch_boundaries = [
    0,
    1,
    8,
    9,
    10,
    11,
    98,
    99,
    100,
    101,
    998,
    999,
    1000,
    1001,
    9998,
    9999,
    10000,
]

rng = random.Random(840084)
representative_generated = sorted({rng.randint(0, 10000) for _ in range(128)})

checked = set(branch_boundaries)
checked.update(documented)
checked.update(representative_generated)
checked.update(range(0, 10001))

mismatches: list[tuple[int, str, str]] = []
for value in sorted(checked):
    oracle = canonical.solve(value)
    observed = candidate.solve(value)
    if observed != oracle:
        mismatches.append((value, oracle, observed))

print(f"documented_examples={sorted(documented.items())}")
print(f"branch_boundaries={branch_boundaries}")
print(f"representative_generated_seed=840084 count={len(representative_generated)}")
print("intended_domain=all integers 0..10000 inclusive")
print(f"unique_inputs_checked={len(checked)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch}")
    raise SystemExit(1)
