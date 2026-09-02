#!/usr/bin/env python3
"""False-conclusion witness for the exact-rational generated numeric semantics."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path


CASE = (6_341_614, 3_071_071, 7_848_477)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def exact_semantics_cents(a: int, b: int, c: int) -> int:
    # The candidate's Heron radicand is
    #   (a+b+c)(-a+b+c)(a-b+c)(a+b-c) / 16.
    # sqrtHundredths multiplies this rational by 10000, takes its exact square
    # root, and rounds the resulting integer hundredths to nearest/ties-even.
    scaled_numerator = (
        (a + b + c)
        * (-a + b + c)
        * (a - b + c)
        * (a + b - c)
        * 10_000
    )
    denominator = 16
    lower = math.isqrt(scaled_numerator // denominator)
    while (lower + 1) ** 2 * denominator <= scaled_numerator:
        lower += 1
    four_value = 4 * scaled_numerator
    midpoint = (2 * lower + 1) ** 2 * denominator
    if four_value > midpoint:
        return lower + 1
    if four_value < midpoint:
        return lower
    return lower if lower % 2 == 0 else lower + 1


canonical = load(Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical")
generated = load(Path("/tmp/audit-work/candidate-fresh/solution.py"), "generated_solution")
a, b, c = CASE
canonical_result = canonical(a, b, c)
generated_result = generated(a, b, c)
k_model_cents = exact_semantics_cents(a, b, c)
k_model_decimal = k_model_cents / 100

print(f"case={CASE}")
print(f"valid_inequalities={(a+b>c, a+c>b, b+c>a)}")
print(f"canonical_python={canonical_result!r}")
print(f"generated_python={generated_result!r}")
print(f"k_exact_model_cents={k_model_cents}")
print(f"k_exact_model_decimal={k_model_decimal!r}")
print(f"python_implementations_agree={canonical_result == generated_result}")
print(f"k_model_agrees_with_python={k_model_decimal == generated_result}")

assert canonical_result == generated_result == 9_268_091_090_989.04
assert k_model_cents == 926_809_109_098_905
assert k_model_decimal == 9_268_091_090_989.05
raise SystemExit(0)
