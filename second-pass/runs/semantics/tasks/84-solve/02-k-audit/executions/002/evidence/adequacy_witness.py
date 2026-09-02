#!/usr/bin/env python3
"""Ground witnesses for the formal precondition and claimed summary."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_solve(path: Path, name: str):
    module_spec = importlib.util.spec_from_file_location(name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.solve


def py_mod(nonnegative: int, divisor: int) -> int:
    return nonnegative % divisor


def decimal_digit(value: int, place: int) -> int:
    if place == 1:
        return py_mod(value, 10)
    assert value >= 0 and place > 1
    return py_mod((value - py_mod(value, place)) // place, 10)


def formal_summary(value: int) -> str:
    assert 0 <= value <= 10000
    digit_sum = sum(decimal_digit(value, place) for place in (1, 10, 100, 1000, 10000))
    return format(digit_sum, "b")


if len(sys.argv) != 3:
    raise SystemExit("usage: adequacy_witness.py CANONICAL_PY SOLUTION_PY")

canonical = load_solve(Path(sys.argv[1]), "witness_canonical")
generated = load_solve(Path(sys.argv[2]), "witness_generated")

for value in (0, 1, 147, 9999, 10000):
    precondition = 0 <= value <= 10000
    claimed = formal_summary(value)
    original = canonical(value)
    submitted = generated(value)
    print(
        f"N={value} precondition={precondition} "
        f"formal={claimed!r} canonical={original!r} submitted={submitted!r}"
    )
    assert precondition
    assert claimed == original == submitted
