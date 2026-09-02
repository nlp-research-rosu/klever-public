#!/usr/bin/env python3
"""Independent differential test for HumanEval 8 sum_product.

Oracle: /reference/canonical.py, imported by absolute path.
Candidate: the clean scratch copy of /candidate/solution.py.
Input scope:
  * documented examples;
  * empty/non-empty loop boundary and sign/zero boundary cases;
  * large arbitrary-precision integers;
  * all lists of lengths 0..5 over {-3,-2,-1,0,1,2,3};
  * 2,000 deterministic pseudorandom lists (length 0..30, values -10^6..10^6).
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "scratch_candidate"
)

named_cases = [
    ("documented-empty", []),
    ("documented-four", [1, 2, 3, 4]),
    ("single-negative", [-1]),
    ("single-zero", [0]),
    ("single-positive", [1]),
    ("zero-middle", [-2, 0, 3]),
    ("two-negatives", [-2, -3, 4]),
    ("alternating", [-3, 2, -1, 1, 0, 5]),
    ("large-positive", [2**63, 2**63 - 1]),
    ("large-negative", [-(2**63), 2**63 - 1]),
    ("arbitrary-precision", [10**100, -(10**50), 3]),
]

tested = 0
mismatches: list[tuple[str, list[int], object, object]] = []


def check(label: str, values: list[int]) -> None:
    global tested
    expected = canonical(values)
    actual = candidate(values)
    tested += 1
    if expected != actual:
        mismatches.append((label, values, expected, actual))


for label, values in named_cases:
    check(label, values)
    print(
        f"NAMED {label}: input={values!r} "
        f"canonical={canonical(values)!r} candidate={candidate(values)!r}"
    )

alphabet = range(-3, 4)
for length in range(6):
    for values in itertools.product(alphabet, repeat=length):
        check(f"exhaustive-len-{length}", list(values))

rng = random.Random(0x8A5)
for index in range(2000):
    length = rng.randrange(31)
    values = [rng.randint(-(10**6), 10**6) for _ in range(length)]
    check(f"random-{index}", values)

print("EXHAUSTIVE_DOMAIN: lengths=0..5 alphabet=-3..3 count=19608")
print("RANDOM_DOMAIN: seed=0x8A5 cases=2000 lengths=0..30 values=-1000000..1000000")
print(f"TOTAL_CASES: {tested}")
print(f"MISMATCHES: {len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH: {mismatch!r}")

sys.exit(1 if mismatches else 0)
