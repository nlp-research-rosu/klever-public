#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import random
import sys


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_a_pile


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function("submitted_solution", Path("/candidate/solution.py"))

documented = [3]
empty_and_boundary = [-3, -1, 0, 1, 2]
branch_representatives = [3, 4, 5, 6, 17, 100, 1000]
rng = random.Random(100_202_607_23)
generated_inputs = sorted({rng.randint(1, 250) for _ in range(40)})

tagged_cases: list[tuple[str, int]] = []
for category, cases in (
    ("documented", documented),
    ("empty_or_boundary", empty_and_boundary),
    ("branch_representative", branch_representatives),
    ("deterministic_generated", generated_inputs),
):
    for case in cases:
        tagged_cases.append((category, case))

failures = 0
print(
    json.dumps(
        {
            "oracle": "/reference/canonical.py:make_a_pile",
            "candidate": "/candidate/solution.py:make_a_pile",
            "seed": 100_202_607_23,
            "documented": documented,
            "empty_and_boundary": empty_and_boundary,
            "branch_representatives": branch_representatives,
            "generated_inputs": generated_inputs,
            "intended_domain": "positive integers",
        },
        sort_keys=True,
    )
)
for category, n in tagged_cases:
    expected = canonical(n)
    actual = generated(n)
    intended_properties = True
    if n > 0:
        intended_properties = (
            len(actual) == n
            and actual[0] == n
            and all(right - left == 2 for left, right in zip(actual, actual[1:]))
            and all(value % 2 == n % 2 for value in actual)
        )
    match = expected == actual
    failures += int(not match or not intended_properties)
    print(
        json.dumps(
            {
                "category": category,
                "n": n,
                "canonical": expected,
                "generated": actual,
                "match": match,
                "intended_properties": intended_properties,
            },
            sort_keys=True,
        )
    )

print(
    json.dumps(
        {
            "cases": len(tagged_cases),
            "mismatches_or_property_failures": failures,
        },
        sort_keys=True,
    )
)
sys.exit(1 if failures else 0)
