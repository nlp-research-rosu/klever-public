#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval 126."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


ROOT = Path("/tmp/audit-work/126-is-sorted-audit-003")
canonical = load_entry(ROOT / "canonical.py", "trusted_canonical_126")
candidate = load_entry(ROOT / "solution.py", "generated_candidate_126")

documented = [
    [5],
    [1, 2, 3, 4, 5],
    [1, 3, 2, 4, 5],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6, 7],
    [1, 3, 2, 4, 5, 6, 7],
    [1, 2, 2, 3, 3, 4],
    [1, 2, 2, 2, 3, 4],
]

boundaries = [
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [1, 1],
    [1, 1, 1],
    [0, 1],
    [1, 0],
    [1, 2, 1],
    [2, 1, 1],
    [1, 2, 2],
    [1, 2, 2, 2],
    [0, 0, 1, 1],
    [0, 1, 1, 0],
    [2**63 - 1],
    [0, 2**63 - 1],
    [2**63 - 1, 0],
]

exhaustive = [
    list(values)
    for length in range(0, 8)
    for values in itertools.product(range(5), repeat=length)
]

rng = random.Random(126)
random_cases = [
    [rng.randrange(0, 10**9) for _ in range(rng.randrange(0, 41))]
    for _ in range(3000)
]

cases = documented + boundaries + exhaustive + random_cases
mismatches = []
true_count = 0
false_count = 0

for index, values in enumerate(cases):
    expected = canonical(values)
    actual = candidate(values)
    if expected:
        true_count += 1
    else:
        false_count += 1
    if type(expected) is not bool or type(actual) is not bool or expected != actual:
        mismatches.append(
            {"index": index, "input": values, "canonical": expected, "candidate": actual}
        )
        if len(mismatches) >= 20:
            break

summary = {
    "intended_domain": "finite lists of nonnegative Python integers",
    "documented_cases": len(documented),
    "boundary_cases": len(boundaries),
    "exhaustive_scope": "all lists of lengths 0..7 over values 0..4",
    "exhaustive_cases": len(exhaustive),
    "random_seed": 126,
    "random_scope": "3000 lists, lengths 0..40, values 0..999999999",
    "random_cases": len(random_cases),
    "total_cases": len(cases),
    "canonical_true": true_count,
    "canonical_false": false_count,
    "mismatch_count": len(mismatches),
    "first_mismatches": mismatches,
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
