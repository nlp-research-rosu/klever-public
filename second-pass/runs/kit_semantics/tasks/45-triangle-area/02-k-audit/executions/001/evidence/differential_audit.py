#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test."""

from __future__ import annotations

import importlib.util
import math
import struct
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path("/tmp/audit-work/45-triangle-area")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, args: tuple[Any, ...]) -> tuple[Any, ...]:
    try:
        value = function(*args)
    except BaseException as error:
        return ("exception", type(error).__module__, type(error).__qualname__, error.args)
    if isinstance(value, float):
        return ("return-float", struct.pack("!d", value).hex())
    if isinstance(value, complex):
        return (
            "return-complex",
            struct.pack("!d", value.real).hex(),
            struct.pack("!d", value.imag).hex(),
        )
    return ("return", type(value).__module__, type(value).__qualname__, repr(value))


def main() -> int:
    canonical = load_module("trusted_canonical", ROOT / "canonical.py").triangle_area
    generated = load_module("generated_solution", ROOT / "solution.py").triangle_area
    cases: list[tuple[str, tuple[Any, ...]]] = [
        ("documented-example", (5, 3)),
        ("zero-zero", (0, 0)),
        ("zero-height", (7, 0)),
        ("zero-side", (0, 11)),
        ("negative-zero", (-0.0, 3)),
        ("positive-integers", (13, 17)),
        ("negative-side", (-4, 3)),
        ("negative-height", (4, -3)),
        ("both-negative", (-4, -3)),
        ("int-float", (3, 2.5)),
        ("float-int", (2.5, 4)),
        ("float-float", (2.5, 1.5)),
        ("subnormal", (math.ulp(0.0), 1.0)),
        ("max-float", (float.fromhex("0x1.fffffffffffffp+1023"), 1.0)),
        ("float-overflow", (float.fromhex("0x1.fffffffffffffp+1023"), 2.0)),
        ("positive-infinity", (math.inf, 2.0)),
        ("negative-infinity", (-math.inf, 2.0)),
        ("nan", (math.nan, 2.0)),
        ("large-int-finite", (2**1023, 1)),
        ("large-int-boundary", (2**1024, 1)),
        ("huge-int-overflow", (10**400, 1)),
        ("bool-bool", (True, False)),
        ("fraction", (Fraction(5, 2), Fraction(3, 2))),
        ("decimal", (Decimal("2.5"), Decimal("3"))),
        ("complex", (2 + 3j, 4 - 1j)),
        ("string-like-out-of-contract", ("5", 3)),
        ("empty-call-out-of-contract", ()),
        ("one-arg-out-of-contract", (1,)),
        ("three-args-out-of-contract", (1, 2, 3)),
    ]
    mismatches = 0
    for name, args in cases:
        expected = outcome(canonical, args)
        actual = outcome(generated, args)
        matches = expected == actual
        mismatches += not matches
        print(f"{name}: args={args!r} canonical={expected!r} generated={actual!r} match={matches}")
    print(
        f"summary cases={len(cases)} documented_examples=1 "
        f"branch_boundaries=0 scalar_zero_boundaries=3 mismatches={mismatches}"
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
