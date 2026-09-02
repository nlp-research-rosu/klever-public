#!/usr/bin/env python3
"""Independent differential test for HumanEval 106-f.

This script is reviewer-authored.  It imports the scratch copies of the
trusted canonical implementation and the submitted implementation by absolute
path.  The generated input sample is deterministic.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


canonical_f = load_entry("trusted_canonical_106f", SCRATCH / "canonical.py")
candidate_f = load_entry("candidate_solution_106f", SCRATCH / "solution.py")

# Empty/boundary values, both parity branches, the prompt example, and sizes
# large enough to exercise multiple accumulator updates.
fixed_inputs = [0, 1, 2, 3, 4, 5, 6, 9, 10, 20, 50, 100]

rng = random.Random(106)
generated_inputs = sorted({rng.randrange(0, 151) for _ in range(100)})
intended_domain_inputs = sorted(set(fixed_inputs + generated_inputs))

mismatches = []
for n in intended_domain_inputs:
    expected = canonical_f(n)
    actual = candidate_f(n)
    if actual != expected:
        mismatches.append((n, expected, actual))

print(f"fixed_inputs={fixed_inputs}")
print(f"generated_seed=106")
print(f"generated_inputs={generated_inputs}")
print(f"intended_domain_case_count={len(intended_domain_inputs)}")
print(f"intended_domain_mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches:
        print(f"MISMATCH={mismatch!r}")
    raise SystemExit(1)

assert candidate_f(5) == [1, 2, 6, 24, 15]
assert candidate_f(0) == []

# Negative integers are reported separately because the formal K entry claim
# excludes them.  Both Python implementations nevertheless return [] there.
negative_observations = {
    n: (canonical_f(n), candidate_f(n)) for n in [-10, -2, -1]
}
print(f"negative_observations={negative_observations}")
print("RESULT=PASS")
