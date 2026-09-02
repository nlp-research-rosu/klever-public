#!/usr/bin/env python3
"""Ground evaluation of the recursive result term stated by SPEC.find-closest."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


def claimed_fold(numbers: list[float]) -> tuple[float, float]:
    # orderedFirst/orderedSecond
    if numbers[0] < numbers[1]:
        first, second = numbers[0], numbers[1]
    else:
        first, second = numbers[1], numbers[0]

    # enumVS plus outerFirst/outerSecond and innerFirst/innerSecond.
    items = list(enumerate(numbers))
    for item1 in items:
        for item2 in items:
            candidate_wins = item1[0] < item2[0] and abs(item2[1] - item1[1]) < abs(
                second - first
            )
            if candidate_wins:
                if item1[1] < item2[1]:
                    first, second = item1[1], item2[1]
                else:
                    first, second = item2[1], item1[1]
    return first, second


canonical = load_entry("canonical_witness", Path("/reference/canonical.py"))
generated = load_entry("generated_witness", Path("/candidate/solution.py"))

cases = [
    [1.0, 2.0],
    [1.0, 9.0, 3.0, 4.0],
    [1.0, 2.0, 3.0, 4.0, 5.0, 2.2],
    [2.0, 2.0],
]

for values in cases:
    formal_result = claimed_fold(values)
    canonical_result = canonical(list(values))
    generated_result = generated(list(values))
    print(
        f"input={values!r} claimed_fold={formal_result!r} "
        f"canonical={canonical_result!r} generated={generated_result!r}"
    )
    assert formal_result == canonical_result == generated_result

print(f"cases={len(cases)} mismatches=0")
