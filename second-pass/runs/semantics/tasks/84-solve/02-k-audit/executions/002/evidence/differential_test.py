#!/usr/bin/env python3
"""Independent exhaustive differential test for HumanEval 84."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_solve(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


if len(sys.argv) != 3:
    raise SystemExit("usage: differential_test.py CANONICAL_PY SOLUTION_PY")

canonical_path = Path(sys.argv[1])
solution_path = Path(sys.argv[2])
canonical = load_solve(canonical_path, "audit_canonical")
generated = load_solve(solution_path, "audit_generated")

documented = {1000: "1", 150: "110", 147: "1100"}
boundaries = [
    0,
    1,
    2,
    8,
    9,
    10,
    11,
    19,
    20,
    89,
    90,
    98,
    99,
    100,
    101,
    109,
    110,
    899,
    900,
    998,
    999,
    1000,
    1001,
    8999,
    9000,
    9998,
    9999,
    10000,
]

for value, expected in documented.items():
    canonical_result = canonical(value)
    generated_result = generated(value)
    assert canonical_result == expected, (value, "canonical", canonical_result, expected)
    assert generated_result == expected, (value, "generated", generated_result, expected)

for value in boundaries:
    canonical_result = canonical(value)
    generated_result = generated(value)
    assert generated_result == canonical_result, (value, generated_result, canonical_result)
    print(f"boundary {value}: {generated_result}")

mismatches: list[tuple[int, str, str]] = []
for value in range(0, 10001):
    canonical_result = canonical(value)
    generated_result = generated(value)
    if generated_result != canonical_result:
        mismatches.append((value, generated_result, canonical_result))

print("documented_examples_checked:", len(documented))
print("boundary_cases_checked:", len(boundaries))
print("exhaustive_domain:", "integers 0..10000 inclusive")
print("exhaustive_cases_checked:", 10001)
print("mismatch_count:", len(mismatches))
if mismatches:
    print("first_mismatches:", mismatches[:20])
    raise SystemExit(1)
