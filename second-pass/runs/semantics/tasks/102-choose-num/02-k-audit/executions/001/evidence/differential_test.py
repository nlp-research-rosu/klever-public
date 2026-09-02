#!/usr/bin/env python3
"""Independent differential and contract-oracle checks for choose_num."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.choose_num


def contract_oracle(x: int, y: int) -> int:
    greatest_even_at_or_below_y = y - (y % 2)
    return greatest_even_at_or_below_y if greatest_even_at_or_below_y >= x else -1


scratch = Path("/tmp/audit-work/102-choose-num")
canonical = load_entry(scratch / "trusted" / "canonical.py", "trusted_canonical")
generated = load_entry(scratch / "solution.py", "generated_solution")

named_cases = {
    "documented-even-below-odd-upper": (12, 15),
    "documented-empty-reversed": (13, 12),
    "minimum-singleton-odd": (1, 1),
    "minimum-to-even": (1, 2),
    "even-singleton": (2, 2),
    "empty-adjacent": (2, 1),
    "even-upper-x-equals-y": (14, 14),
    "even-upper-x-just-above-y": (15, 14),
    "odd-upper-predecessor-at-x": (14, 15),
    "odd-upper-x-equals-y": (15, 15),
    "odd-upper-x-above-y": (16, 15),
    "large-even-singleton": (10**12, 10**12),
    "large-odd-singleton": (10**12 + 1, 10**12 + 1),
}

inputs: list[tuple[int, int, str]] = [
    (x, y, f"named:{name}") for name, (x, y) in named_cases.items()
]
inputs.extend(
    (x, y, "exhaustive-grid-1..200")
    for x in range(1, 201)
    for y in range(1, 201)
)

rng = random.Random(102)
inputs.extend(
    (
        rng.randint(1, 10**12),
        rng.randint(1, 10**12),
        "seeded-random-positive-int",
    )
    for _ in range(5000)
)

mismatches: list[tuple[int, int, int, int, int, str]] = []
brute_force_checks = 0
for x, y, source in inputs:
    expected = canonical(x, y)
    actual = generated(x, y)
    oracle = contract_oracle(x, y)
    brute = oracle
    if 0 <= y - x <= 500:
        candidates = [value for value in range(x, y + 1) if value % 2 == 0]
        brute = max(candidates) if candidates else -1
        brute_force_checks += 1
    if expected != actual or expected != oracle or oracle != brute:
        mismatches.append((x, y, expected, actual, oracle, source))

print("domain: positive Python integers")
print("oracle: trusted canonical.py plus greatest-even formula; bounded cases also enumerated")
print(f"documented_and_boundary_cases={len(named_cases)}")
print("exhaustive_grid=x,y in [1,200]")
print("seeded_random_cases=5000 seed=102 endpoints in [1,10^12]")
print(f"bounded_bruteforce_oracle_checks={brute_force_checks}")
print(f"total_cases={len(inputs)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH", mismatch)

raise SystemExit(1 if mismatches else 0)
