#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs submitted solution."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decimal_to_binary


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("submitted_solution", Path("/candidate/solution.py"))

documented_and_boundaries = [15, 32, 0, 1, 2, 3, 4, 7, 8, 9]
exhaustive_small = list(range(0, 4097))
powers = []
for exponent in range(0, 1025):
    power = 1 << exponent
    powers.extend(value for value in (power - 1, power, power + 1) if value >= 0)

rng = random.Random(790079)
generated_cases = [rng.getrandbits(rng.randrange(0, 1025)) for _ in range(2000)]
cases = list(dict.fromkeys(documented_and_boundaries + exhaustive_small + powers + generated_cases))

mismatches = []
for value in cases:
    expected = canonical(value)
    actual = generated(value)
    if actual != expected:
        mismatches.append((value, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"documented_and_boundary_cases={documented_and_boundaries}")
print("small_domain=all integers 0..4096")
print("power_boundaries=2**k-1, 2**k, 2**k+1 for k=0..1024")
print("random_seed=790079 random_nonnegative_integers=2000 max_bits=1024")
print(f"unique_cases={len(cases)} mismatches={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", mismatch)
assert not mismatches
print("DIFFERENTIAL=PASS")
