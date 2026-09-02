#!/usr/bin/env python3
"""Ground substitutions for the formal sortVS/strangeResult summary."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/task70")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_ground", ROOT / "canonical.py").strange_sort_list
generated = load("generated_solution_ground", ROOT / "solution.py").strange_sort_list


def ins_vs(value: int, values: list[int]) -> list[int]:
    if not values:
        return [value]
    if value <= values[0]:
        return [value, *values]
    return [values[0], *ins_vs(value, values[1:])]


def sort_vs(values: list[int]) -> list[int]:
    if not values:
        return []
    return ins_vs(values[0], sort_vs(values[1:]))


def strange_prefix(sorted_values: list[int], count: int) -> list[int]:
    out: list[int] = []
    size = len(sorted_values)
    for index in range(count):
        if index % 2 == 0:
            out.append(sorted_values[index // 2])
        else:
            out.append(sorted_values[size - (index // 2) - 1])
    return out


cases = [
    [],
    [4, 1, 3, 2],
    [3, -1, 3, 2, 0],
    [5, 5, 5, 5],
]
for values in cases:
    sorted_values = sort_vs(list(values))
    formal = strange_prefix(sorted_values, len(sorted_values))
    canonical_value = canonical(list(values))
    generated_value = generated(list(values))
    print(
        f"INPUT={values!r} "
        f"sortVS={sorted_values!r} "
        f"strangeResult={formal!r} "
        f"canonical={canonical_value!r} "
        f"generated={generated_value!r}"
    )
    assert formal == canonical_value == generated_value

print(f"GROUND_SUBSTITUTION=PASS cases={len(cases)}")
