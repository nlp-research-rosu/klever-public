#!/usr/bin/env python3
"""Independent differential test for HumanEval problem 97."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


EVIDENCE_DIR = Path("/audit-output/evidence")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("submitted_solution", Path("/tmp/audit-work/candidate-src/solution.py"))

documented = [(148, 412), (19, 28), (2020, 1851), (14, -15)]
zero_and_boundaries = [
    (0, 0),
    (0, 1),
    (1, 0),
    (-1, 0),
    (0, -1),
    (9, 9),
    (9, 10),
    (10, 9),
    (10, 10),
    (10, 11),
    (11, 10),
    (-9, 9),
    (-10, 9),
    (-11, 9),
    (9, -9),
    (9, -10),
    (9, -11),
    (-9, -9),
    (-10, -10),
    (-11, -11),
    (10**100 - 1, -(10**100 - 1)),
    (10**100, -(10**100)),
    (10**100 + 1, -(10**100 + 1)),
]

# Exhaust every pair around twenty consecutive modulo-10 boundaries.
exhaustive = [(a, b) for a in range(-100, 101) for b in range(-100, 101)]

# Deterministic broad samples across Python's unbounded integer domain.
rng = random.Random(970097)
generated_inputs = [
    (rng.randrange(-(10**80), 10**80), rng.randrange(-(10**80), 10**80))
    for _ in range(5000)
]

tagged_cases = (
    [("documented", a, b) for a, b in documented]
    + [("zero-boundary", a, b) for a, b in zero_and_boundaries]
    + [("exhaustive--100..100", a, b) for a, b in exhaustive]
    + [("seeded-random", a, b) for a, b in generated_inputs]
)

inputs_path = EVIDENCE_DIR / "differential-inputs.json"
inputs_path.write_text(
    json.dumps(
        {
            "seed": 970097,
            "random_range": ["-10**80 inclusive", "10**80 exclusive"],
            "cases": tagged_cases,
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

mismatches = []
category_counts: dict[str, int] = {}
for category, a, b in tagged_cases:
    category_counts[category] = category_counts.get(category, 0) + 1
    expected = canonical(a, b)
    actual = generated(a, b)
    if expected != actual:
        mismatches.append(
            {
                "category": category,
                "a": a,
                "b": b,
                "canonical": expected,
                "generated": actual,
            }
        )

print(f"oracle=/reference/canonical.py:multiply")
print(f"subject=/tmp/audit-work/candidate-src/solution.py:multiply")
print(f"category_counts={category_counts}")
print(f"total_cases={len(tagged_cases)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], indent=2))
    raise SystemExit(1)
