#!/usr/bin/env python3
"""Independent behavioral comparison for HumanEval 124-valid-date."""

from __future__ import annotations

import importlib.util
import random
import string
from collections import Counter
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "scratch_generated", Path("/tmp/audit-work/reconstruction/solution.py")
)


def strict_contract_oracle(date: str) -> bool:
    """Independent direct reading of the prompt's literal mm-dd-yyyy contract."""
    if len(date) != 10 or date[2] != "-" or date[5] != "-":
        return False
    digit_positions = (0, 1, 3, 4, 6, 7, 8, 9)
    if any(not ("0" <= date[i] <= "9") for i in digit_positions):
        return False
    month = 10 * (ord(date[0]) - ord("0")) + ord(date[1]) - ord("0")
    day = 10 * (ord(date[3]) - ord("0")) + ord(date[4]) - ord("0")
    if not 1 <= month <= 12 or day < 1:
        return False
    limit = 29 if month == 2 else 30 if month in (4, 6, 9, 11) else 31
    return day <= limit


documented = [
    ("03-11-2000", True),
    ("15-01-2012", False),
    ("04-0-2040", False),
    ("06-04-2020", True),
    ("06/04/2020", False),
]

boundary = [
    "",
    "-",
    "00-01-2000",
    "01-00-2000",
    "01-01-0000",
    "01-29-2000",
    "01-30-2000",
    "01-31-2000",
    "01-32-2000",
    "02-00-2000",
    "02-01-2000",
    "02-28-2000",
    "02-29-2000",
    "02-30-2000",
    "04-29-2000",
    "04-30-2000",
    "04-31-2000",
    "06-30-2000",
    "09-30-2000",
    "11-30-2000",
    "12-31-9999",
    "13-01-2000",
    "1-1-2000",
    "01-1-2000",
    "1-01-2000",
    "01-01-20",
    "01-01-20000",
    " 03-11-2000 ",
    "03-11-+2000",
    "03--1-2000",
    "03-11--001",
    "03/11/2000",
    "03-11-20x0",
    "٠٣-١١-٢٠٠٠",
    "03-11-２０00",
    "ab-cd-efgh",
]

formatted = [
    f"{month:02d}-{day:02d}-{year}"
    for month in range(0, 14)
    for day in range(0, 33)
    for year in ("0000", "2000", "9999")
]

rng = random.Random(124)
alphabet = string.digits + string.ascii_letters + "-/ +"
random_malformed = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 14)))
    for _ in range(2000)
]

cases: dict[str, set[str]] = {
    "documented": {s for s, _ in documented},
    "boundary": set(boundary),
    "strict_formatted_grid": set(formatted),
    "seeded_malformed": set(random_malformed),
}

expected_documented = dict(documented)
all_mismatches: list[tuple[str, str, object, object, object]] = []
candidate_contract_mismatches: list[tuple[str, str, object, object]] = []
counts: Counter[tuple[str, str]] = Counter()

for category, values in cases.items():
    for value in sorted(values):
        try:
            canonical_result: object = canonical(value)
        except Exception as err:  # pragma: no cover - recorded as an observable
            canonical_result = f"EXC:{type(err).__name__}:{err}"
        try:
            generated_result: object = generated(value)
        except Exception as err:  # pragma: no cover - recorded as an observable
            generated_result = f"EXC:{type(err).__name__}:{err}"
        contract_result = strict_contract_oracle(value)
        counts[(category, "cases")] += 1
        if canonical_result != generated_result:
            counts[(category, "canonical_generated_mismatch")] += 1
            all_mismatches.append(
                (
                    category,
                    value,
                    canonical_result,
                    generated_result,
                    contract_result,
                )
            )
        if generated_result != contract_result:
            counts[(category, "generated_contract_mismatch")] += 1
            candidate_contract_mismatches.append(
                (category, value, generated_result, contract_result)
            )

for value, expected in documented:
    actual = generated(value)
    if actual != expected:
        raise AssertionError(
            f"documented example {value!r}: generated={actual!r}, expected={expected!r}"
        )

print("ORACLES")
print("canonical=/reference/canonical.py:valid_date")
print("generated=/tmp/audit-work/reconstruction/solution.py:valid_date")
print("contract=independent strict mm-dd-yyyy implementation in this script")
print("RANDOM_SEED=124")
print("INPUT_SCOPE")
for category in cases:
    print(
        f"{category}: cases={counts[(category, 'cases')]} "
        f"canonical_generated_mismatches="
        f"{counts[(category, 'canonical_generated_mismatch')]} "
        f"generated_contract_mismatches="
        f"{counts[(category, 'generated_contract_mismatch')]}"
    )

print(f"TOTAL_CANONICAL_GENERATED_MISMATCHES={len(all_mismatches)}")
print(f"TOTAL_GENERATED_CONTRACT_MISMATCHES={len(candidate_contract_mismatches)}")
print("FIRST_CANONICAL_GENERATED_MISMATCHES")
for row in all_mismatches[:100]:
    print(repr(row))
print("FIRST_GENERATED_CONTRACT_MISMATCHES")
for row in candidate_contract_mismatches[:100]:
    print(repr(row))

if candidate_contract_mismatches:
    raise SystemExit(1)
