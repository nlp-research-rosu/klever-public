#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential for HumanEval/150."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.x_or_y


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_function("generated_candidate", Path("/candidate/solution.py"))

# Explicit branch and contract boundaries, then a broad deterministic integer sample.
boundary_n = [-25, -3, -1, 0, 1, 2, 3, 4, 7, 9, 15, 16, 17, 25, 97, 101]
sample_n = list(range(-25, 501))
payloads: list[tuple[Any, Any]] = [
    (34, 12),
    (8, 5),
    (0, 1),
    (-7, 99),
    ("x-value", "y-value"),
    ([1, 2], [3]),
]

cases: list[tuple[int, Any, Any, str]] = [
    (7, 34, 12, "documented-example-prime"),
    (15, 8, 5, "documented-example-composite"),
]
for n in boundary_n:
    for x, y in payloads:
        cases.append((n, x, y, "boundary"))
for n in sample_n:
    x = n * 17 - 4
    y = 1003 - n * 13
    cases.append((n, x, y, "generated-range"))

mismatches: list[tuple[int, Any, Any, Any, Any, str]] = []
exceptions: list[tuple[int, str, str]] = []
for n, x, y, label in cases:
    try:
        expected = canonical(n, x, y)
        actual = candidate(n, x, y)
    except Exception as error:  # Evidence should retain any asymmetric crash.
        exceptions.append((n, label, repr(error)))
        continue
    if actual != expected:
        mismatches.append((n, x, y, expected, actual, label))

print("oracle=/reference/canonical.py:x_or_y")
print("candidate=/candidate/solution.py:x_or_y")
print(f"boundary_n={boundary_n}")
print(f"generated_n_range={sample_n[0]}..{sample_n[-1]}")
print(f"payload_pairs={len(payloads)}")
print(f"cases={len(cases)}")
print(f"exceptions={len(exceptions)}")
print(f"mismatches={len(mismatches)}")
for item in exceptions[:40]:
    print(f"EXCEPTION {item!r}")
for item in mismatches[:80]:
    print(f"MISMATCH {item!r}")
if len(mismatches) > 80:
    print(f"MISMATCH_OUTPUT_TRUNCATED remaining={len(mismatches) - 80}")

# A mismatch is evidence to judge, not an infrastructure/script failure.
raise SystemExit(0)
