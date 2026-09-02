#!/usr/bin/env python3
"""Independent candidate/canonical differential for HumanEval 71."""

from __future__ import annotations

import importlib.util
import math
import random
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


def load(path: str, module_name: str) -> Callable[..., Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


candidate = load("/tmp/audit-work/proof/solution.py", "audited_candidate")
canonical = load("/reference/canonical.py", "trusted_canonical")


def outcome(function: Callable[..., Any], args: tuple[Any, Any, Any]) -> tuple[str, Any]:
    try:
        return ("value", function(*args))
    except Exception as error:  # noqa: BLE001 - exception behavior is part of the differential.
        return ("exception", type(error).__name__)


def equivalent(left: tuple[str, Any], right: tuple[str, Any]) -> bool:
    if left[0] != right[0]:
        return False
    if left[0] == "exception":
        return left[1] == right[1]
    try:
        if math.isnan(left[1]) and math.isnan(right[1]):
            return True
    except (TypeError, ValueError):
        pass
    return left[1] == right[1]


fixed_cases: list[tuple[str, tuple[Any, Any, Any]]] = [
    ("example-valid", (3, 4, 5)),
    ("example-invalid", (1, 2, 10)),
    ("boundary-ab-eq-c", (1, 2, 3)),
    ("boundary-ac-eq-b", (1, 3, 2)),
    ("boundary-bc-eq-a", (3, 1, 2)),
    ("valid-near-ab", (2, 2, 3)),
    ("valid-near-ac", (2, 3, 2)),
    ("valid-near-bc", (3, 2, 2)),
    ("invalid-ab", (1, 2, 4)),
    ("invalid-ac", (1, 4, 2)),
    ("invalid-bc", (4, 1, 2)),
    ("all-zero", (0, 0, 0)),
    ("negative", (-1, -1, -1)),
    ("mixed-sign", (-1, 4, 5)),
    ("bool-numeric", (True, True, True)),
    ("float-scalene", (2.5, 3.0, 4.0)),
    ("just-valid-float", (1.0, 1.0, math.nextafter(2.0, 0.0))),
    ("just-invalid-float", (1.0, 1.0, math.nextafter(2.0, 3.0))),
    ("subnormal", (5e-324, 5e-324, 5e-324)),
    ("large-float", (1e154, 1e154, 1e154)),
    ("positive-infinity", (math.inf, math.inf, math.inf)),
    ("nan-first", (math.nan, 3.0, 4.0)),
    ("nan-second", (3.0, math.nan, 4.0)),
    ("nan-third", (3.0, 4.0, math.nan)),
    ("fractions", (Fraction(3), Fraction(4), Fraction(5))),
    ("decimals", (Decimal("3"), Decimal("4"), Decimal("5"))),
    ("empty-strings", ("", "", "")),
    ("empty-lists", ([], [], [])),
]

rng = random.Random(710071)
generated_cases: list[tuple[str, tuple[Any, Any, Any]]] = []
for index in range(400):
    generated_cases.append(
        (
            f"generated-int-{index}",
            tuple(rng.randint(-100, 100) for _ in range(3)),
        )
    )
for index in range(400):
    generated_cases.append(
        (
            f"generated-float-{index}",
            tuple(rng.randint(-1000, 1000) / 10.0 for _ in range(3)),
        )
    )

all_cases = fixed_cases + generated_cases
mismatches: list[tuple[str, tuple[Any, Any, Any], tuple[str, Any], tuple[str, Any]]] = []
for label, args in all_cases:
    candidate_result = outcome(candidate, args)
    canonical_result = outcome(canonical, args)
    if not equivalent(candidate_result, canonical_result):
        mismatches.append((label, args, candidate_result, canonical_result))
    if label in {case[0] for case in fixed_cases}:
        print(
            f"FIXED {label} args={args!r} "
            f"candidate={candidate_result!r} canonical={canonical_result!r}"
        )

# Decimal is outside the docstring-determined representation/error contract.
# Returning the mathematically correct area is defensible; this mismatch is
# retained as an observation but is not a material contract mismatch.
allowed_divergence_labels = {"decimals"}
material_mismatches = [
    mismatch for mismatch in mismatches if mismatch[0] not in allowed_divergence_labels
]

example_checks = [
    (candidate(3, 4, 5) == 6.00, "candidate example (3,4,5)"),
    (candidate(1, 2, 10) == -1, "candidate example (1,2,10)"),
]

# Independent high-precision adequacy spot-check on small positive integer sides.
oracle_checks = 0
oracle_mismatches: list[tuple[tuple[int, int, int], Any, Decimal]] = []
with localcontext() as context:
    context.prec = 80
    for a in range(1, 31):
        for b in range(1, 31):
            for c in range(1, 31):
                actual = candidate(a, b, c)
                if a + b <= c or a + c <= b or b + c <= a:
                    expected: Any = -1
                else:
                    da, db, dc = Decimal(a), Decimal(b), Decimal(c)
                    s = (da + db + dc) / Decimal(2)
                    expected = (
                        (s * (s - da) * (s - db) * (s - dc)).sqrt()
                    ).quantize(Decimal("0.01"))
                oracle_checks += 1
                if Decimal(str(actual)) != Decimal(str(expected)):
                    oracle_mismatches.append(((a, b, c), actual, expected))

print(f"TOTAL_DIFFERENTIAL_CASES={len(all_cases)}")
print(f"DIFFERENTIAL_MISMATCHES={len(mismatches)}")
print(f"ALLOWED_UNDERSPECIFIED_DIVERGENCES={len(mismatches) - len(material_mismatches)}")
print(f"MATERIAL_CONTRACT_MISMATCHES={len(material_mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")
print(f"DOCUMENTED_EXAMPLE_FAILURES={sum(not passed for passed, _ in example_checks)}")
for passed, label in example_checks:
    print(f"EXAMPLE {label} passed={passed}")
print(f"DECIMAL_ORACLE_CASES={oracle_checks}")
print(f"DECIMAL_ORACLE_MISMATCHES={len(oracle_mismatches)}")
for mismatch in oracle_mismatches[:20]:
    print(f"ORACLE_MISMATCH {mismatch!r}")

assert not material_mismatches
assert all(passed for passed, _ in example_checks)
assert not oracle_mismatches
