#!/usr/bin/env python3
"""Ground the K postcondition's digit equations and compare both Python functions."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verification = Path("/tmp/audit-work/candidate/verification.k").read_text()
canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "witness_canonical")
candidate = load(Path("/tmp/audit-work/candidate/solution.py"), "witness_candidate")


def digit_table(name: str) -> dict[int, str]:
    pattern = re.compile(
        rf"(?ms)^\s*rule\s+{re.escape(name)}\((\d+)\)\s*=>\s*"
        rf"(.*?)\s*\[concrete\]\s*$"
    )
    table: dict[int, str] = {}
    for digit, term in pattern.findall(verification):
        codepoints = [int(value) for value in re.findall(r"iCons\((\d+),", term)]
        table[int(digit)] = "".join(chr(value) for value in codepoints)
    return table


tables = {
    "thousands": digit_table("thousandsDigit"),
    "hundreds": digit_table("hundredsDigit"),
    "tens": digit_table("tensDigit"),
    "ones": digit_table("onesDigit"),
}

if set(tables["thousands"]) != set(range(2)):
    raise RuntimeError(f"incomplete thousands equations: {tables['thousands']}")
for place in ("hundreds", "tens", "ones"):
    if set(tables[place]) != set(range(10)):
        raise RuntimeError(f"incomplete {place} equations: {tables[place]}")


def grounded_roman_spec(number: int) -> str:
    return (
        tables["thousands"][number // 1000]
        + tables["hundreds"][(number % 1000) // 100]
        + tables["tens"][(number % 100) // 10]
        + tables["ones"][number % 10]
    )


witnesses = [1, 4, 9, 19, 152, 426, 944, 1000]
failures: list[str] = []
for number in range(1, 1001):
    claimed = grounded_roman_spec(number)
    canonical_result = canonical.int_to_mini_roman(number)
    candidate_result = candidate.int_to_mini_roman(number)
    if claimed != canonical_result or claimed != candidate_result:
        failures.append(
            f"N={number}: K={claimed!r}, canonical={canonical_result!r}, "
            f"candidate={candidate_result!r}"
        )

print("entry_precondition_example=N=1 (1 <= N <= 1000)")
print(f"parsed_K_digit_tables={tables}")
for number in witnesses:
    print(
        f"N={number}: K_postcondition={grounded_roman_spec(number)!r}; "
        f"canonical={canonical.int_to_mini_roman(number)!r}; "
        f"candidate={candidate.int_to_mini_roman(number)!r}"
    )
print("checked_ground_instances=1000")
print(f"mismatch_count={len(failures)}")
for failure in failures[:50]:
    print(f"MISMATCH {failure}")
if failures:
    raise SystemExit(1)
