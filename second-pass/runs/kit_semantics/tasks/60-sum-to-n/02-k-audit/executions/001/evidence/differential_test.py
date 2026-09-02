#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_to_n


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"),
    "candidate_solution",
)

# Examples, the guard boundaries, adjacent values, and deterministic generated
# values across small, medium, and very large magnitudes.
documented = [30, 100, 5, 10, 1]
boundaries = [-10, -3, -2, -1, 0, 1, 2, 3, 10]
rng = random.Random(0x60)
generated = [rng.randint(-10_000, 10_000) for _ in range(400)]
generated += [
    -(10**k) for k in range(1, 7)
] + [
    10**k for k in range(1, 7)
]
inputs = documented + boundaries + generated

mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected:
        mismatches.append((n, expected, actual))

print(
    f"documented={len(documented)} boundaries={len(boundaries)} "
    f"generated={len(generated)} total={len(inputs)} "
    f"mismatches={len(mismatches)}"
)
print("boundary_results")
for n in boundaries:
    print(f"n={n} canonical={canonical(n)} candidate={candidate(n)}")
if mismatches:
    print(f"first_mismatches={mismatches[:10]}")
    raise SystemExit(1)
print("DIFFERENTIAL_PASS")
