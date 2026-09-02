#!/usr/bin/env python3
"""Independent differential check of trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_function(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_odd_collatz


canonical = load_function(Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical")
candidate = load_function(Path("/tmp/audit-work/candidate-src/solution.py"), "candidate_solution")

# n=1 is the loop-skipping boundary; 2 is the first even branch; 3 is the
# first odd branch above 1; 5 is the documented example; 27 is the long case.
named_cases = [1, 2, 3, 4, 5, 6, 7, 19, 27, 97, 871, 6171]
rng = random.Random(123_20260726)
generated_cases = [rng.randint(1, 10_000) for _ in range(200)]
exhaustive_small = list(range(1, 1001))
cases = list(dict.fromkeys(named_cases + exhaustive_small + generated_cases))

mismatches = []
for n in cases:
    expected = canonical(n)
    actual = candidate(n)
    if expected != actual:
        mismatches.append((n, expected, actual))

print(f"named_cases={named_cases}")
print("empty_valid_input_case=not_applicable (contract input is a positive integer)")
print(f"small_exhaustive_range=1..1000")
print(f"generated_seed=12320260726 generated_count={len(generated_cases)} generated_range=1..10000")
print(f"unique_cases={len(cases)}")
for n in named_cases:
    print(f"case n={n}: canonical={canonical(n)} candidate={candidate(n)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch}")
raise SystemExit(1 if mismatches else 0)
