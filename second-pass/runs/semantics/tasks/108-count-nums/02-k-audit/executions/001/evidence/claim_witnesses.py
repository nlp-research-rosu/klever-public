#!/usr/bin/env python3
"""Ground witnesses for the final claim and its mathematical summaries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module(
    "canonical_108_witness", "/tmp/audit-work/audit-108/trusted/canonical.py"
)
generated = load_module(
    "generated_108_witness", "/tmp/audit-work/audit-108/source/solution.py"
)


def signed_digit_contract(n: int) -> int:
    text = str(abs(n))
    digits = [int(char) for char in text]
    if n < 0:
        digits[0] = -digits[0]
    return sum(digits)


def count_positive_contract(values: list[int]) -> int:
    return sum(1 for value in values if signed_digit_contract(value) > 0)


samples = [
    [],
    [-12, -11, 0, 10],
    [-1, 11, -11],
    [1, 1, 2],
    [-999, -123, -21, -12, -11, -10, -1, 0, 1, 10, 12, 100],
]

print("Every sample is a finite ValSeq of Int values, so allInts(VS)=true.")
for sample in samples:
    formal_result = count_positive_contract(sample)
    canonical_result = canonical.count_nums(sample)
    generated_result = generated.count_nums(sample)
    print(
        f"arr={sample!r} countPositive={formal_result} "
        f"canonical={canonical_result} generated={generated_result}"
    )
    if formal_result != canonical_result or formal_result != generated_result:
        raise SystemExit(1)

helper_values = [-1203, -12, -11, -1, 0, 1, 10, 1203]
for value in helper_values:
    contract_result = signed_digit_contract(value)
    generated_result = generated.signed_digit_sum(value)
    print(
        f"n={value} signedDigitSum_contract={contract_result} "
        f"generated_helper={generated_result}"
    )
    if contract_result != generated_result:
        raise SystemExit(1)
