#!/usr/bin/env python3
"""Independent differential test for HumanEval 122.

The oracle is the trusted /reference/canonical.py.  The generated entry point is
loaded from the clean scratch copy, never from candidate bytecode or caches.
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path
from typing import Any


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add_elements


def outcome(function, arr: list[int], k: int) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(list(arr), k)}
    except Exception as error:  # deliberately compare out-of-domain behavior too
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "generated_solution", Path("/tmp/audit-work/122-add-elements/solution.py")
)

cases: list[dict[str, Any]] = [
    {
        "name": "documented-example",
        "domain": "intended",
        "arr": [111, 21, 3, 4000, 5, 6, 7, 8, 9],
        "k": 4,
    },
    {"name": "empty-k0", "domain": "outside", "arr": [], "k": 0},
    {"name": "empty-k1", "domain": "outside", "arr": [], "k": 1},
    {"name": "singleton-zero", "domain": "intended", "arr": [0], "k": 1},
    {"name": "singleton-negative-one", "domain": "intended", "arr": [-1], "k": 1},
    {"name": "singleton-negative-nine", "domain": "intended", "arr": [-9], "k": 1},
    {"name": "singleton-negative-ten", "domain": "intended", "arr": [-10], "k": 1},
    {"name": "singleton-negative-ninety-nine", "domain": "intended", "arr": [-99], "k": 1},
    {"name": "singleton-negative-hundred", "domain": "intended", "arr": [-100], "k": 1},
    {"name": "singleton-positive-nine", "domain": "intended", "arr": [9], "k": 1},
    {"name": "singleton-positive-ten", "domain": "intended", "arr": [10], "k": 1},
    {"name": "singleton-positive-ninety-nine", "domain": "intended", "arr": [99], "k": 1},
    {"name": "singleton-positive-hundred", "domain": "intended", "arr": [100], "k": 1},
    {
        "name": "all-branch-boundaries",
        "domain": "intended",
        "arr": [-101, -100, -99, -10, -9, -1, 0, 9, 10, 99, 100, 101],
        "k": 12,
    },
    {
        "name": "k-prefix-boundary",
        "domain": "intended",
        "arr": [21, -10, 4000, 3],
        "k": 1,
    },
    {
        "name": "max-length-max-k",
        "domain": "intended",
        "arr": [(-1 if index % 2 else 1) * index for index in range(1, 101)],
        "k": 100,
    },
]

# Exhaustively isolate the value predicate around and beyond both thresholds.
for value in range(-150, 151):
    cases.append(
        {
            "name": f"exhaustive-singleton-{value}",
            "domain": "intended",
            "arr": [value],
            "k": 1,
        }
    )

# Deterministic representative arrays exercise prefix lengths, mixtures, and size 100.
rng = random.Random(122)
pool = [-1000, -101, -100, -99, -50, -10, -9, -1, 0, 1, 9, 10, 42, 99, 100, 101, 1000]
for index in range(100):
    length = rng.randint(1, 20)
    arr = [rng.choice(pool) if rng.random() < 0.7 else rng.randint(-5000, 5000) for _ in range(length)]
    cases.append(
        {
            "name": f"generated-{index:03d}",
            "domain": "intended",
            "arr": arr,
            "k": rng.randint(1, length),
        }
    )

results: list[dict[str, Any]] = []
for case in cases:
    expected = outcome(canonical, case["arr"], case["k"])
    actual = outcome(generated, case["arr"], case["k"])
    results.append(
        {
            **case,
            "canonical": expected,
            "generated": actual,
            "match": expected == actual,
        }
    )

mismatches = [result for result in results if not result["match"]]
intended_mismatches = [
    result for result in mismatches if result["domain"] == "intended"
]
report = {
    "oracle": "/reference/canonical.py:add_elements",
    "generated": "/tmp/audit-work/122-add-elements/solution.py:add_elements",
    "seed": 122,
    "case_count": len(results),
    "intended_case_count": sum(result["domain"] == "intended" for result in results),
    "mismatch_count": len(mismatches),
    "intended_mismatch_count": len(intended_mismatches),
    "named_cases": [
        result for result in results if not result["name"].startswith(("generated-", "exhaustive-"))
    ],
    "mismatches": mismatches,
}
print(json.dumps(report, indent=2, sort_keys=True))
sys.exit(1 if intended_mismatches else 0)
