#!/usr/bin/env python3
"""Independent differential check: trusted canonical versus submitted Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random
import sys


SCRATCH = Path("/tmp/audit-work/change-base-audit-20260726")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


canonical = load_entry(SCRATCH / "reference/canonical.py", "trusted_canonical")
generated = load_entry(SCRATCH / "candidate/solution.py", "submitted_solution")

documented = [(8, 3), (8, 2), (7, 2)]
boundary: list[tuple[int, int]] = []
for base in range(2, 10):
    for x in [-10, -2, -1, 0, 1, base - 1, base, base + 1,
              base * base - 1, base * base, base * base + 1]:
        boundary.append((x, base))

exhaustive_small = [(x, base) for base in range(2, 10) for x in range(1, 513)]

rng = random.Random(440026)
generated_positive = [
    (rng.randrange(1, 10**12 + 1), rng.randrange(2, 10))
    for _ in range(1000)
]
generated_nonpositive = [
    (rng.randrange(-10**6, 1), rng.randrange(2, 10))
    for _ in range(250)
]

cases = documented + boundary + exhaustive_small + generated_positive + generated_nonpositive

mismatches: list[tuple[int, int, str, str]] = []
for x, base in cases:
    expected = canonical(x, base)
    actual = generated(x, base)
    if expected != actual:
        mismatches.append((x, base, expected, actual))

print("oracle=/tmp/audit-work/change-base-audit-20260726/reference/canonical.py")
print("subject=/tmp/audit-work/change-base-audit-20260726/candidate/solution.py")
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundary)}")
print(f"exhaustive_small_positive_cases={len(exhaustive_small)}")
print(f"seed=440026")
print(f"generated_positive_cases={len(generated_positive)}")
print(f"generated_nonpositive_cases={len(generated_nonpositive)}")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
print(f"positive_mismatch_count={sum(x > 0 for x, _, _, _ in mismatches)}")
print(f"zero_mismatch_count={sum(x == 0 for x, _, _, _ in mismatches)}")
print(f"negative_mismatch_count={sum(x < 0 for x, _, _, _ in mismatches)}")
for index, (x, base, expected, actual) in enumerate(mismatches[:20], 1):
    print(
        f"mismatch[{index}]: x={x} base={base} "
        f"canonical={expected!r} generated={actual!r}"
    )

sys.exit(1 if mismatches else 0)
