#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval/2."""

from __future__ import annotations

import importlib.util
import math
import random
import struct
import sys
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load(Path("/tmp/audit-work/fresh/solution.py"), "candidate_solution")

documented = [3.5]
boundaries = [
    math.nextafter(0.0, math.inf),
    sys.float_info.min * sys.float_info.epsilon,
    sys.float_info.min,
    math.nextafter(1.0, 0.0),
    1.0,
    math.nextafter(1.0, math.inf),
    math.nextafter(2.0, 0.0),
    2.0,
    math.nextafter(2.0, math.inf),
    2.0**52 - 0.5,
    2.0**52,
    sys.float_info.max,
]
grid = [
    whole + fraction / 32.0
    for whole in range(0, 129)
    for fraction in range(1, 32)
]

rng = random.Random(0x2A11D17)
generated = []
while len(generated) < 4096:
    bits = rng.getrandbits(64) & 0x7FFF_FFFF_FFFF_FFFF
    value = struct.unpack(">d", bits.to_bytes(8, "big"))[0]
    if math.isfinite(value) and value > 0.0:
        generated.append(value)

cases = documented + boundaries + grid + generated
mismatches = []
for number in cases:
    expected = canonical.truncate_number(number)
    actual = candidate.truncate_number(number)
    if actual != expected:
        mismatches.append((number, expected, actual))

print(f"documented={len(documented)}")
print(f"positive_finite_boundaries={len(boundaries)}")
print(f"positive_finite_grid={len(grid)}")
print(f"positive_finite_generated={len(generated)}")
print(f"total={len(cases)} mismatches={len(mismatches)}")
print("example_3_5", candidate.truncate_number(3.5))
print("smallest_positive", boundaries[0], candidate.truncate_number(boundaries[0]))
print("below_one", boundaries[3], candidate.truncate_number(boundaries[3]))
print("at_one", candidate.truncate_number(1.0))
print("above_one", boundaries[5], candidate.truncate_number(boundaries[5]))
print("max_finite", candidate.truncate_number(sys.float_info.max))

if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    raise SystemExit(1)

