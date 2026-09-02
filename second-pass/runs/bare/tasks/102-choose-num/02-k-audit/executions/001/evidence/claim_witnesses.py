#!/usr/bin/env python3
"""Satisfying witnesses and concrete substitutions for all eight entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_humaneval_102_witness", Path("/reference/canonical.py"))
generated = load_module("generated_solution_102_witness", Path("/tmp/audit-work/solution.py"))


def contract(x: int, y: int, result: int) -> bool:
    no_even = x > y or (x == y and x % 2 != 0)
    return (result == -1 and no_even) or (
        result != -1
        and x <= result <= y
        and result % 2 == 0
        and y < result + 2
    )


rows = [
    (1, "X>Y exact sentinel", 2, 1, -1, lambda x, y: x > y),
    (2, "X<=Y and even Y exact Y", 1, 2, 2, lambda x, y: x <= y and y % 2 == 0),
    (3, "X<Y and odd Y exact Y-1", 2, 3, 2, lambda x, y: x < y and y % 2 != 0),
    (4, "X=Y and odd Y exact sentinel", 1, 1, -1, lambda x, y: x == y and y % 2 != 0),
    (5, "X>Y contract true", 2, 1, -1, lambda x, y: x > y),
    (6, "X<=Y and even Y contract true", 1, 2, 2, lambda x, y: x <= y and y % 2 == 0),
    (7, "X<Y and odd Y contract true", 2, 3, 2, lambda x, y: x < y and y % 2 != 0),
    (8, "X=Y and odd Y contract true", 1, 1, -1, lambda x, y: x == y and y % 2 != 0),
]

for number, description, x, y, claimed_result, guard in rows:
    assert x > 0 and y > 0 and guard(x, y)
    trusted = canonical.choose_num(x, y)
    actual = generated.choose_num(x, y)
    assertion = trusted == claimed_result == actual
    if number >= 5:
        assertion = assertion and contract(x, y, actual)
    print(
        f"claim={number} description={description!r} witness=({x},{y}) "
        f"claimed={claimed_result} canonical={trusted} generated={actual} "
        f"obligation={assertion}"
    )
    if not assertion:
        raise SystemExit(1)
