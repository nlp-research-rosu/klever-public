#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/53."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/53-add-clean/solution.py")


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(CANONICAL, "trusted_humaneval_53_canonical")
generated = load(GENERATED, "candidate_humaneval_53_solution")

cases: list[tuple[int, int, str]] = [
    (2, 3, "prompt-example"),
    (5, 7, "prompt-example"),
    (0, 0, "zero-boundary"),
    (0, 1, "zero-boundary"),
    (1, 0, "zero-boundary"),
    (-1, 0, "sign-boundary"),
    (0, -1, "sign-boundary"),
    (-1, 1, "cancellation"),
    (1, -1, "cancellation"),
    (-(2**63), -1, "beyond-fixed-width"),
    (2**63 - 1, 1, "beyond-fixed-width"),
    (-(2**255), 2**255, "arbitrary-precision"),
]

for x in range(-8, 9):
    for y in range(-8, 9):
        cases.append((x, y, "exhaustive-small-grid"))

rng = random.Random(530053)
for _ in range(128):
    x = rng.getrandbits(rng.randrange(0, 257))
    y = rng.getrandbits(rng.randrange(0, 257))
    if rng.randrange(2):
        x = -x
    if rng.randrange(2):
        y = -y
    cases.append((x, y, "deterministic-generated"))

mismatches = 0
for index, (x, y, category) in enumerate(cases):
    expected = canonical.add(x, y)
    actual = generated.add(x, y)
    match = type(actual) is type(expected) and actual == expected
    print(
        json.dumps(
            {
                "index": index,
                "category": category,
                "x": x,
                "y": y,
                "canonical": expected,
                "generated": actual,
                "exact_match": match,
            },
            sort_keys=True,
        )
    )
    mismatches += not match

print(f"case_count={len(cases)}")
print(f"mismatch_count={mismatches}")
raise SystemExit(1 if mismatches else 0)
