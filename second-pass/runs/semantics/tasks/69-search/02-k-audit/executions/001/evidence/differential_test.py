#!/usr/bin/env python3
"""Independent differential test for HumanEval 69-search.

The two modules are loaded from explicit, read-only provenance paths.  The
generated cases are deterministic, so this file fully records the input scope.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_search(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search


canonical = load_search(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_search(Path("/tmp/audit-work/69-search/solution.py"), "generated_solution")


def outcome(function: Callable[[list[int]], int], values: list[int]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(values.copy())}
    except Exception as error:  # Deliberately record out-of-contract behavior.
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


documented_and_boundary = [
    ("example-1", [4, 1, 2, 2, 3, 1]),
    ("example-2", [1, 2, 2, 3, 3, 3, 4, 4, 4]),
    ("example-3", [5, 5, 4, 4, 4]),
    ("smallest-positive-qualifies", [1]),
    ("single-nonqualifier", [2]),
    ("equal-threshold", [2, 2]),
    ("just-below-threshold", [3, 3]),
    ("two-qualifiers-greatest-wins", [2, 2, 3, 3, 3]),
    ("repeated-qualifier-does-not-lower-result", [3, 3, 3, 1, 1]),
    ("large-singleton", [100]),
    ("large-equal-threshold", [7, 7, 7, 7, 7, 7, 7]),
    ("empty-outside-contract", []),
    ("zero-outside-contract", [0]),
    ("negative-outside-contract", [-1, -1]),
]

print("explicit cases:")
intended_explicit_mismatches = 0
outside_contract_differences = 0
for label, values in documented_and_boundary:
    left = outcome(canonical, values)
    right = outcome(generated, values)
    in_contract = bool(values) and all(isinstance(value, int) and value > 0 for value in values)
    equal = left == right
    if in_contract and not equal:
        intended_explicit_mismatches += 1
    if not in_contract and not equal:
        outside_contract_differences += 1
    print(json.dumps({
        "label": label,
        "input": values,
        "in_contract": in_contract,
        "canonical": left,
        "generated": right,
        "equal": equal,
    }, sort_keys=True))

exhaustive_count = 0
exhaustive_mismatch_count = 0
exhaustive_mismatches: list[dict[str, Any]] = []
for length in range(1, 7):
    for values_tuple in itertools.product(range(1, 6), repeat=length):
        values = list(values_tuple)
        left = outcome(canonical, values)
        right = outcome(generated, values)
        exhaustive_count += 1
        if left != right:
            exhaustive_mismatch_count += 1
            if len(exhaustive_mismatches) < 20:
                exhaustive_mismatches.append({"input": values, "canonical": left, "generated": right})

rng = random.Random(690069)
random_count = 500
random_mismatch_count = 0
random_mismatches: list[dict[str, Any]] = []
for _ in range(random_count):
    values = [rng.randint(1, 50) for _ in range(rng.randint(1, 40))]
    left = outcome(canonical, values)
    right = outcome(generated, values)
    if left != right:
        random_mismatch_count += 1
        if len(random_mismatches) < 20:
            random_mismatches.append({"input": values, "canonical": left, "generated": right})

summary = {
    "explicit_intended_mismatches": intended_explicit_mismatches,
    "outside_contract_differences": outside_contract_differences,
    "exhaustive_domain": "all lists of lengths 1..6 over values 1..5",
    "exhaustive_count": exhaustive_count,
    "exhaustive_mismatch_count": exhaustive_mismatch_count,
    "exhaustive_first_mismatches": exhaustive_mismatches,
    "random_seed": 690069,
    "random_domain": "500 lists, lengths 1..40, values 1..50",
    "random_count": random_count,
    "random_mismatch_count": random_mismatch_count,
    "random_first_mismatches": random_mismatches,
}
print("summary:")
print(json.dumps(summary, indent=2, sort_keys=True))

if intended_explicit_mismatches or exhaustive_mismatches or random_mismatches:
    sys.exit(1)
