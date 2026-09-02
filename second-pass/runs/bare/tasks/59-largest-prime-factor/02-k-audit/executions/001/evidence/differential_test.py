#!/usr/bin/env python3
"""Independent differential test for HumanEval 59.

The oracle is loaded from the trusted /reference/canonical.py.  The candidate
implementation is loaded from the clean scratch copy, not from /candidate.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_prime_factor


oracle = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/review-59/src/solution.py"), "generated_solution"
)


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


documented = [13195, 2048]
boundary_and_branches = [
    4,   # smallest intended input; loop true, divisibility true, then loop false
    6,   # factor 2 divides, final residual 3
    8,   # repeated divisibility-true branch
    9,   # divisibility-false at 2, true at 3
    10,
    12,
    15,
    16,
    21,
    25,  # equality boundary factor*factor == n
    27,
    49,
    77,
    121,
]

# A fixed-seed generated sample of intended-domain values plus exhaustive small
# composites.  This remains finite evidence, not a universal proof.
rng = random.Random(590059)
generated_inputs = []
while len(generated_inputs) < 100:
    n = rng.randint(4, 20_000)
    if not is_prime(n):
        generated_inputs.append(n)

exhaustive_small = [n for n in range(4, 1001) if not is_prime(n)]
inputs = sorted(
    set(documented + boundary_and_branches + generated_inputs + exhaustive_small)
)

mismatches = []
for n in inputs:
    expected = oracle(n)
    actual = generated(n)
    if actual != expected:
        mismatches.append((n, expected, actual))

print(f"intended-domain cases: {len(inputs)}")
print(f"minimum input: {min(inputs)}")
print(f"maximum input: {max(inputs)}")
print(f"mismatches: {len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH", mismatch)

# The task has one scalar parameter, so there is no empty-container case.
# Record behavior immediately outside the stated domain rather than treating it
# as correctness evidence.
outside = [0, 1, 2, 3, 5, 7]
print("empty-container case: not applicable (scalar integer input)")
print("outside-domain observations:")
for n in outside:
    print(f"  n={n}: canonical={oracle(n)}, generated={generated(n)}")

raise SystemExit(1 if mismatches else 0)
