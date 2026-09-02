#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval 105."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_function(path: Path, module_name: str) -> Callable[[list[int]], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    assert isinstance(module, ModuleType)
    spec.loader.exec_module(module)
    function = getattr(module, "by_length")
    return function


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(
    Path("/tmp/audit-work/source/solution.py"), "scratch_generated_solution"
)

documented = [
    [2, 1, 1, 4, 5, 8, 2, 3],
    [],
    [1, -1, 55],
]

# Every target digit, both invalid neighbors, duplicates, mixed order, and all
# per-element count traversal branches are represented in these boundary cases.
boundary = [
    [digit] for digit in range(1, 10)
] + [
    [-1],
    [0],
    [10],
    [55],
    [1, 1],
    [9, 9],
    [0, 1, 9, 10],
    [9, 1, 5, 5, 0, -1, 10],
    list(range(-2, 12)),
    list(range(11, -3, -1)),
    [1, 9] * 20,
]

# Exhaust the Cartesian product through length 4 over all valid digits and
# representative invalid integers on both sides of the valid interval.
alphabet = [-2, -1, 0, *range(1, 10), 10, 11, 55]
exhaustive = (
    list(items)
    for length in range(5)
    for items in itertools.product(alphabet, repeat=length)
)

rng = random.Random(105)
generated_cases = [
    [rng.randint(-100, 100) for _ in range(rng.randint(0, 60))]
    for _ in range(500)
]
generated_cases.extend(
    [
        [-(10**100), 1, 9, 10**100],
        [digit for digit in range(1, 10) for _ in range(30)],
        [digit for digit in range(9, 0, -1) for _ in range(30)],
    ]
)

inputs_path = Path("/audit-output/evidence/differential_inputs.jsonl")
mismatches: list[dict[str, object]] = []
case_count = 0
with inputs_path.open("w", encoding="utf-8") as inputs_stream:
    all_cases = itertools.chain(documented, boundary, exhaustive, generated_cases)
    for case_id, values in enumerate(all_cases):
        expected = canonical(values.copy())
        actual = generated(values.copy())
        record = {"id": case_id, "input": values}
        inputs_stream.write(json.dumps(record, separators=(",", ":")) + "\n")
        case_count += 1
        if actual != expected:
            mismatches.append(
                {
                    **record,
                    "canonical": expected,
                    "generated": actual,
                }
            )
            if len(mismatches) >= 20:
                break

print("oracle=/reference/canonical.py:by_length")
print("candidate=/tmp/audit-work/source/solution.py:by_length")
print(f"documented_cases={len(documented)}")
print(f"explicit_boundary_cases={len(boundary)}")
print("exhaustive_scope=all integer lists length 0..4 over " + repr(alphabet))
print(f"seeded_random_cases={len(generated_cases)} seed=105")
print(f"executed_cases={case_count}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches, indent=2))
    raise SystemExit(1)
