#!/usr/bin/env python3
"""Exhibit concrete satisfying states and instantiate each formal result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/92-any-int")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


canonical = load("trusted_canonical", SCRATCH / "canonical.py")
generated = load("submitted_solution", SCRATCH / "solution.py")


def sum_condition(x: int, y: int, z: int) -> bool:
    return x + y == z or x + z == y or y + z == x


witnesses = [
    ("integer-true", (5, 2, 7), True, "sumCondition(5,2,7)"),
    ("integer-false", (3, 2, 2), False, "sumCondition(3,2,2)"),
    ("nonint-x", (3.5, 2, 7), False, "not isIntV(Float(3.5))"),
    ("nonint-y", (5, 2.5, 7), False, "not isIntV(Float(2.5))"),
    ("nonint-z", (5, 2, 7.0), False, "not isIntV(Float(7.0))"),
]

for label, args, formal, precondition in witnesses:
    if label.startswith("integer"):
        formal = sum_condition(*args)
    trusted_value = canonical(*args)
    generated_value = generated(*args)
    print(
        f"{label}: args={args!r}; precondition={precondition}; "
        f"formal_result={formal!r}; canonical={trusted_value!r}; "
        f"generated={generated_value!r}"
    )
    assert formal is trusted_value is generated_value

print("ALL_WITNESSES_SATISFY_PRECONDITIONS_AND_RESULTS=true")
