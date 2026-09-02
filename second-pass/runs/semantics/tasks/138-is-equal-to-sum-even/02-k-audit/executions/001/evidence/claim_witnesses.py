#!/usr/bin/env python3
"""Concrete satisfying inputs for each entry claim and its result formula."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[int], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_equal_to_sum_even


canonical = load_entry(Path("/reference/canonical.py"), "trusted_witness_canonical")
generated = load_entry(
    Path("/tmp/audit-work/review-138/solution.py"), "witness_candidate_solution"
)


def py_mod(a: int, b: int) -> int:
    return ((a % b) + b) % b


claims = [
    ("universal", 8, True, lambda n: True),
    ("even-at-least-eight", 8, True, lambda n: n >= 8 and py_mod(n, 2) == 0),
    ("below-eight", 7, False, lambda n: n < 8),
    (
        "nonzero-remainder-at-least-eight",
        9,
        False,
        lambda n: n >= 8 and py_mod(n, 2) != 0,
    ),
]

for name, value, claimed, precondition in claims:
    assert precondition(value), (name, value)
    canonical_value = canonical(value)
    generated_value = generated(value)
    formula_value = value >= 8 and py_mod(value, 2) == 0
    assert canonical_value == generated_value == formula_value == claimed
    print(
        f"{name}: N={value} precondition=true "
        f"canonical={canonical_value} generated={generated_value} "
        f"main_formula={formula_value} claimed={claimed}"
    )
