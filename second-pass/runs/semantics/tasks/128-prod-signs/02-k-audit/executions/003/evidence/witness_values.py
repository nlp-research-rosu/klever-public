#!/usr/bin/env python3
"""Ground witnesses for the two entry claims and their formal postconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prod_signs


canonical = load_function("trusted_canonical_witness", Path("/reference/canonical.py"))
generated = load_function("candidate_solution_witness", Path("/candidate/solution.py"))


def magnitude_sum(values: list[int]) -> int:
    acc = 0
    for value in values:
        acc = acc - value if value < 0 else acc + value
    return acc


def sign_product(values: list[int]) -> int:
    acc = 1
    for value in values:
        if value < 0:
            acc = -acc
        elif value == 0:
            acc = 0
    return acc


for values in ([], [-2, 0, 3], [-2, -3]):
    formal = None if not values else magnitude_sum(values) * sign_product(values)
    trusted = canonical(values)
    candidate = generated(values)
    print(
        f"input={values!r} all_ints={all(type(v) is int for v in values)} "
        f"formal={formal!r} canonical={trusted!r} generated={candidate!r}"
    )
    assert formal == trusted == candidate
