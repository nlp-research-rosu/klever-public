#!/usr/bin/env python3
"""Independent differential test of trusted canonical vs submitted solution."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reviewer-002/scratch")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


canonical = load_entry("trusted_canonical", SCRATCH / "canonical.py")
generated = load_entry("submitted_solution", SCRATCH / "solution.py")

# Examples, empty/negative cases, divisibility boundaries, digit-7 boundaries,
# and thresholds around representative qualifying values.
curated = [
    -100,
    -5,
    -1,
    0,
    1,
    2,
    7,
    8,
    10,
    11,
    12,
    13,
    14,
    21,
    22,
    23,
    25,
    26,
    27,
    28,
    49,
    50,
    51,
    76,
    77,
    78,
    79,
    80,
    99,
    100,
    101,
    116,
    117,
    118,
    143,
    144,
    175,
    176,
    177,
    178,
    769,
    770,
    771,
    777,
    778,
    1000,
    1001,
    10_000,
    20_000,
]

# Exhaustive small interval plus deterministic representative generated inputs.
rng = random.Random(36_071_113)
random_cases = [rng.randint(-1000, 20_000) for _ in range(1000)]
all_cases = sorted(set(curated + list(range(-20, 501)) + random_cases))

mismatches: list[tuple[int, object, object]] = []
print(f"oracle={SCRATCH / 'canonical.py'}")
print(f"implementation={SCRATCH / 'solution.py'}")
print("domain=int samples")
print("exhaustive_interval=-20..500 inclusive")
print("random_seed=36071113 random_draws=1000 range=-1000..20000 inclusive")
print(f"curated_inputs={curated}")
print("CURATED_RESULTS_BEGIN")
for n in curated:
    expected = canonical(n)
    actual = generated(n)
    print(f"n={n} canonical={expected} generated={actual}")
    if expected != actual:
        mismatches.append((n, expected, actual))
print("CURATED_RESULTS_END")

for n in all_cases:
    expected = canonical(n)
    actual = generated(n)
    if expected != actual:
        mismatches.append((n, expected, actual))

print(f"distinct_cases={len(all_cases)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for n, expected, actual in mismatches[:50]:
        print(f"MISMATCH n={n} canonical={expected} generated={actual}")
    raise SystemExit(1)
print("RESULT=PASS")
