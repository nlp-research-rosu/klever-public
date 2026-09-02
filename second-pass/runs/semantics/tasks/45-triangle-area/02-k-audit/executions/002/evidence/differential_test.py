#!/usr/bin/env python3
"""Independent differential check against the trusted HumanEval canonical."""

from __future__ import annotations

import importlib.util
import math
import random
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


def load_function(module_name: str, path: Path) -> Callable[..., Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function("candidate_solution", Path("/tmp/audit-work/proof/solution.py"))


def outcome(fn: Callable[..., Any], args: tuple[Any, ...]) -> tuple[str, Any, str]:
    try:
        result = fn(*args)
        if isinstance(result, float) and math.isnan(result):
            normalized: Any = "NaN"
        elif isinstance(result, float) and result == 0.0:
            normalized = ("zero", math.copysign(1.0, result))
        else:
            normalized = result
        return ("value", normalized, type(result).__qualname__)
    except Exception as err:  # the exception class is part of the comparison
        return ("exception", type(err).__qualname__, str(err))


documented_and_boundaries: list[tuple[str, tuple[Any, ...]]] = [
    ("documented example", (5, 3)),
    ("both zero", (0, 0)),
    ("zero base", (0, 9)),
    ("zero height", (9, 0)),
    ("unit", (1, 1)),
    ("negative base", (-3, 6)),
    ("negative height", (3, -6)),
    ("both negative", (-3, -6)),
    ("large exact", (2**53, 2)),
    ("very large conversion boundary", (10**308, 2)),
    ("positive floats", (5.5, 3.25)),
    ("small positive floats", (1.0e-300, 2.0e-20)),
    ("positive infinity", (math.inf, 2.0)),
    ("not-a-number", (math.nan, 2.0)),
    ("booleans", (True, False)),
    ("empty call / arity boundary", ()),
    ("one argument / arity boundary", (5,)),
    ("three arguments / arity boundary", (5, 3, 1)),
]

randomizer = random.Random(450045)
generated_integers = [
    (
        f"generated integer #{index}",
        (randomizer.randint(-(10**18), 10**18), randomizer.randint(-(10**18), 10**18)),
    )
    for index in range(2000)
]
generated_floats = [
    (
        f"generated finite float #{index}",
        (randomizer.uniform(-1.0e100, 1.0e100), randomizer.uniform(-1.0e100, 1.0e100)),
    )
    for index in range(500)
]
ordinary_cases = documented_and_boundaries + generated_integers + generated_floats

mismatches: list[tuple[str, tuple[Any, ...], tuple[str, Any, str], tuple[str, Any, str]]] = []
for label, args in ordinary_cases:
    expected = outcome(canonical, args)
    actual = outcome(generated, args)
    if expected != actual:
        mismatches.append((label, args, expected, actual))

print("oracle=/reference/canonical.py:triangle_area")
print("subject=/tmp/audit-work/proof/solution.py:triangle_area")
print("seed=450045")
print(f"ordinary_case_count={len(ordinary_cases)}")
print(f"ordinary_mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"ORDINARY_MISMATCH={mismatch!r}")

# These broader Python numeric protocols are recorded separately because the
# natural-language prompt does not type the parameters. They expose the precise
# behavioral difference between a literal 2.0 and a literal 2.
protocol_cases = [
    ("Decimal operands", (Decimal("5.5"), Decimal("3.0"))),
    ("Fraction operands", (Fraction(1, 3), Fraction(1, 1))),
]
protocol_mismatches = []
for label, args in protocol_cases:
    expected = outcome(canonical, args)
    actual = outcome(generated, args)
    if expected != actual:
        protocol_mismatches.append((label, args, expected, actual))
    print(f"PROTOCOL_CASE label={label!r} canonical={expected!r} generated={actual!r}")
print(f"protocol_case_count={len(protocol_cases)}")
print(f"protocol_mismatch_count={len(protocol_mismatches)}")

if mismatches:
    raise SystemExit(1)
print("ORDINARY_DIFFERENTIAL=PASS")
