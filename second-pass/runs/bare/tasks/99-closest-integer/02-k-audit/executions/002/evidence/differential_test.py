#!/usr/bin/env python3
"""Independent contract, canonical, and candidate differential test."""

from __future__ import annotations

import importlib.util
import random
from decimal import Decimal
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


canonical = load_entry(Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical")
candidate = load_entry(Path("/tmp/audit-work/candidate/solution.py"), "candidate_solution")


def contract_oracle(text: str) -> int:
    """Nearest integer with exact half ties away from zero."""
    value = Decimal(text)
    if not value.is_finite():
        raise ValueError("the source contract is restricted to finite numbers")
    numerator, denominator = value.as_integer_ratio()
    magnitude, remainder = divmod(abs(numerator), denominator)
    rounded = magnitude + int(2 * remainder >= denominator)
    return rounded if numerator >= 0 else -rounded


def outcome(fn, text: str):
    try:
        return ("value", fn(text))
    except Exception as error:  # Test records boundary exception behavior.
        return ("exception", type(error).__name__, str(error))


cases: list[tuple[str, str]] = [
    ("example", "10"),
    ("example", "15.3"),
    ("example", "14.5"),
    ("example", "-14.5"),
    ("empty-boundary-outside-contract", ""),
    ("zero-boundary", "0"),
    ("zero-boundary", "-0"),
    ("positive-branch", "0.49"),
    ("positive-half", "0.5"),
    ("positive-above-half", "0.51"),
    ("negative-branch", "-0.49"),
    ("negative-half", "-0.5"),
    ("negative-below-half", "-0.51"),
    ("integer", "999"),
    ("trailing-zeros", "2.500"),
    ("leading-point", ".5"),
    ("leading-point", "-.5"),
    ("explicit-plus", "+2.5"),
    ("scientific", "1e2"),
    ("scientific-half", "2.5e0"),
    ("scientific-half", "-2.5E+0"),
    ("scientific-exact-integer", "1.50e2"),
    ("high-precision-below", "1.499999999999999999999999"),
    ("high-precision-above", "1.500000000000000000000001"),
    ("large-half", "9007199254740992.5"),
    ("large-negative-half", "-9007199254740992.5"),
]

rng = random.Random(990099)
for _ in range(240):
    coefficient = rng.randint(-10**9, 10**9)
    scale = rng.randint(0, 8)
    if scale == 0:
        text = str(coefficient)
    else:
        sign = "-" if coefficient < 0 else ""
        digits = str(abs(coefficient)).zfill(scale + 1)
        text = f"{sign}{digits[:-scale]}.{digits[-scale:]}"
    cases.append(("generated-fixed-decimal", text))

for coefficient in range(-35, 36):
    cases.append(("generated-scientific", f"{coefficient}e-1"))

candidate_contract_mismatches = 0
canonical_contract_mismatches = 0
candidate_canonical_mismatches = 0
outside_contract_checked = 0
for index, (category, text) in enumerate(cases):
    can = outcome(canonical, text)
    got = outcome(candidate, text)
    if category == "empty-boundary-outside-contract":
        outside_contract_checked += 1
        print(f"OUTSIDE index={index} category={category} input={text!r} canonical={can!r} candidate={got!r}")
        assert can[0] == "exception" and got[0] == "exception"
        continue
    expected = ("value", contract_oracle(text))
    if got != expected:
        candidate_contract_mismatches += 1
        print(f"CANDIDATE_CONTRACT_MISMATCH index={index} category={category} input={text!r} expected={expected!r} actual={got!r}")
    if can != expected:
        canonical_contract_mismatches += 1
        print(f"CANONICAL_CONTRACT_MISMATCH index={index} category={category} input={text!r} expected={expected!r} actual={can!r}")
    if got != can:
        candidate_canonical_mismatches += 1
        print(f"CANDIDATE_CANONICAL_DIVERGENCE index={index} category={category} input={text!r} canonical={can!r} candidate={got!r}")

print(f"valid_cases={len(cases) - outside_contract_checked}")
print(f"outside_contract_cases={outside_contract_checked}")
print(f"candidate_contract_mismatches={candidate_contract_mismatches}")
print(f"canonical_contract_mismatches={canonical_contract_mismatches}")
print(f"candidate_canonical_mismatches={candidate_canonical_mismatches}")
assert candidate_contract_mismatches == 0
