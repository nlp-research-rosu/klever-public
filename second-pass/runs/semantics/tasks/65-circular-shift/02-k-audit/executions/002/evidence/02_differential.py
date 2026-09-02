#!/usr/bin/env python3
"""Independent differential test against the trusted HumanEval canonical."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module(
    "scratch_candidate", Path("/tmp/audit-work/reconstruction/solution.py")
)

# The two documented examples, zero/single-digit cases, both sides of the
# shift==len branch boundary, negative-shift boundaries, negative x, and very
# large integers.
curated = [
    (12, 1),
    (12, 2),
    (12, 0),
    (12, 3),
    (12, -1),
    (12, -2),
    (12, -3),
    (0, 0),
    (0, 1),
    (0, 2),
    (0, -1),
    (5, 0),
    (5, 1),
    (5, 2),
    (5, -1),
    (100, 0),
    (100, 1),
    (100, 2),
    (100, 3),
    (100, 4),
    (100, -1),
    (100, -3),
    (-1, 0),
    (-1, 1),
    (-1, 2),
    (-1, 3),
    (-1, -1),
    (-123, 0),
    (-123, 1),
    (-123, 4),
    (-123, 5),
    (-123, -1),
    (-123, -4),
    (10**80 + 987654321, 0),
    (10**80 + 987654321, 1),
    (10**80 + 987654321, 81),
    (10**80 + 987654321, 82),
    (10**80 + 987654321, -1),
]

# Exhaustive representative grid over 47 x values and shifts -12..20.
grid_x = list(range(-20, 21)) + [-999, -100, -10, 100, 999, 10**20 + 7]
grid = [(x, shift) for x in grid_x for shift in range(-12, 21)]

# A deterministic broader sample over arbitrary-size signed decimal integers.
rng = random.Random(650065)
generated = []
for _ in range(1000):
    digits = rng.randint(1, 120)
    magnitude = rng.randrange(10 ** (digits - 1), 10**digits)
    x = -magnitude if rng.randrange(2) else magnitude
    shift = rng.randint(-150, 180)
    generated.append((x, shift))

cases = curated + grid + generated
serialized = json.dumps(cases, separators=(",", ":")).encode()
print("oracle=/reference/canonical.py:circular_shift")
print("candidate=/tmp/audit-work/reconstruction/solution.py:circular_shift")
print(f"curated_count={len(curated)}")
print(
    "grid_scope=x in range(-20,21) plus "
    "[-999,-100,-10,100,999,10**20+7], shift in range(-12,21)"
)
print(f"grid_count={len(grid)}")
print(
    "generated_scope=seed 650065; 1000 signed decimal integers with 1..120 digits; "
    "shift uniformly in [-150,180]"
)
print(f"generated_count={len(generated)}")
print(f"all_case_count={len(cases)}")
print(f"case_list_sha256={hashlib.sha256(serialized).hexdigest()}")

mismatches: list[tuple[int, int, str, str]] = []
nonnegative_mismatches = 0
negative_mismatches = 0
for x, shift in cases:
    expected = canonical.circular_shift(x, shift)
    actual = candidate.circular_shift(x, shift)
    if actual != expected:
        mismatches.append((x, shift, expected, actual))
        if shift >= 0:
            nonnegative_mismatches += 1
        else:
            negative_mismatches += 1

print(f"mismatch_count={len(mismatches)}")
print(f"nonnegative_shift_mismatch_count={nonnegative_mismatches}")
print(f"negative_shift_mismatch_count={negative_mismatches}")
for index, (x, shift, expected, actual) in enumerate(mismatches[:40], 1):
    print(
        f"MISMATCH[{index}] x={x!r} shift={shift} "
        f"canonical={expected!r} candidate={actual!r}"
    )
if len(mismatches) > 40:
    print(f"... {len(mismatches) - 40} additional mismatches omitted from bounded log")

sys.exit(1 if mismatches else 0)
