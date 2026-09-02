#!/usr/bin/env python3
"""Evaluate concrete witnesses for each formal entry-claim partition."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def py_mod(x: int, n: int) -> int:
    return ((x % n) + n) % n


def positive_power_loop(x: int, n: int) -> bool:
    while py_mod(x, n) == 0:
        x = x // n
    return x == 1


def formal_simple_power(x: int, n: int) -> bool:
    if x == 1:
        return True
    if x < 1:
        return False
    if n <= 1:
        return False
    return positive_power_loop(x, n)


if len(sys.argv) != 3:
    raise SystemExit("usage: claim_witnesses.py TRUSTED_CANONICAL GENERATED_SOLUTION")

canonical = load_module("trusted_canonical_witness", Path(sys.argv[1]))
generated = load_module("generated_solution_witness", Path(sys.argv[2]))

witnesses = [
    ("function-one", 1, 4),
    ("function-below-one", 0, 2),
    ("function-degenerate-base", 2, 1),
    ("function-positive-domain-true", 8, 2),
    ("function-positive-domain-false", 3, 2),
]

for label, x, n in witnesses:
    formal = formal_simple_power(x, n)
    generated_result = generated.is_simple_power(x, n)
    canonical_result = canonical.is_simple_power(x, n)
    print(
        f"{label}: x={x} n={n} formal={formal} "
        f"generated={generated_result} canonical={canonical_result}"
    )
    assert formal == generated_result == canonical_result

print("loop-correct: X=8 N=2 satisfies N>1; positivePowerLoop(8,2)=True")
assert positive_power_loop(8, 2) is True
print(f"witnesses_passed={len(witnesses) + 1}")
