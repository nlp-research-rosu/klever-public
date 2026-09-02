#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py vs submitted solution.py."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if len(sys.argv) != 3:
    raise SystemExit("usage: differential_test.py CANONICAL.py SOLUTION.py")

canonical_module = load_module("trusted_canonical", Path(sys.argv[1]))
solution_module = load_module("submitted_solution", Path(sys.argv[2]))

# Documented examples, all base/recurrence branch boundaries, and deterministic
# generated representatives. The source contract has no collection-valued
# "empty" input; n=0 is its lower boundary.
documented = [1, 5, 8]
boundaries = [0, 1, 2, 3, 4]
generator = random.Random(630063)
generated = [generator.randrange(0, 21) for _ in range(12)]
cases = list(dict.fromkeys(documented + boundaries + generated + [10, 15, 20]))

print(f"documented={documented}")
print(f"boundaries={boundaries}")
print(f"generated_seed=630063 generated={generated}")
print(f"ordered_cases={cases}")

mismatches = []
for n in cases:
    canonical_value = canonical_module.fibfib(n)
    submitted_value = solution_module.fibfib(n)
    matches = canonical_value == submitted_value
    print(
        f"n={n} canonical={canonical_value} submitted={submitted_value}"
        f" match={matches}"
    )
    if not matches:
        mismatches.append((n, canonical_value, submitted_value))

print(f"case_count={len(cases)} mismatch_count={len(mismatches)}")
if mismatches:
    print(f"mismatches={mismatches}")
raise SystemExit(0 if not mismatches else 1)
