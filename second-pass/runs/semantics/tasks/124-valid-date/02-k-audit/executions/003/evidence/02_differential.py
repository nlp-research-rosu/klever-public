#!/usr/bin/env python3
"""Independent differential and prompt-contract tests for 124-valid-date."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
from pathlib import Path


WORK = Path("/tmp/audit-work/124-valid-date")
INPUT_RECORD = Path("/audit-output/evidence/02_differential_inputs.tsv")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", WORK / "trusted_canonical.py").valid_date
generated = load("generated_solution", WORK / "solution.py").valid_date


def prompt_oracle(date: str) -> bool:
    """Direct executable reading of mm-dd-yyyy and the stated month/day limits."""
    if len(date) != 10:
        return False
    if date[2] != "-" or date[5] != "-":
        return False
    digit_positions = (0, 1, 3, 4, 6, 7, 8, 9)
    if any(not ("0" <= date[i] <= "9") for i in digit_positions):
        return False
    month = int(date[:2])
    day = int(date[3:5])
    if month < 1 or month > 12 or day < 1:
        return False
    if month == 2:
        return day <= 29
    if month in (4, 6, 9, 11):
        return day <= 30
    return day <= 31


cases: list[tuple[str, str]] = []


def add(category: str, value: str) -> None:
    cases.append((category, value))


for value in [
    "03-11-2000",
    "15-01-2012",
    "04-0-2040",
    "06-04-2020",
    "06/04/2020",
]:
    add("documented-example", value)

for value in [
    "",
    " ",
    "-",
    "00-01-2000",
    "01-00-2000",
    "01-01-0000",
    "01-31-0000",
    "01-32-0000",
    "02-28-2000",
    "02-29-2000",
    "02-30-2000",
    "04-30-2000",
    "04-31-2000",
    "06-30-2000",
    "06-31-2000",
    "09-30-2000",
    "09-31-2000",
    "11-30-2000",
    "11-31-2000",
    "12-31-9999",
    "13-01-2000",
    "03/11/2000",
    "03--1-2000",
    "03-11+2000",
    "03-11-20000",
    "3-1-2000",
    " 03-11-2000",
    "03-11-2000 ",
    "\t03-11-2000\n",
    "０３-１１-２０００",
    "03-11-２０００",
    "03-11-+2000",
    "03-11--001",
]:
    add("boundary-or-malformed", value)

# Exhaust every two-digit month/day pair for two representative four-digit years.
for month, day, year in itertools.product(range(100), range(100), ("0000", "2000")):
    add("all-two-digit-month-day", f"{month:02d}-{day:02d}-{year}")

# Explicit length boundaries with deterministic representative data.
for length in range(0, 15):
    add("length-boundary", "x" * length)
    add("length-boundary", ("01-01-2000" + "x" * length)[:length])

# Deterministic generated inputs from a documented alphabet.
rng = random.Random(124)
alphabet = string.digits + string.ascii_letters + "-/ +\t"
for _ in range(5000):
    length = rng.randrange(0, 16)
    add("seeded-generated", "".join(rng.choice(alphabet) for _ in range(length)))

# Deduplicate while retaining the earliest category and deterministic order.
seen: set[str] = set()
unique_cases: list[tuple[str, str]] = []
for category, value in cases:
    if value not in seen:
        seen.add(value)
        unique_cases.append((category, value))

canonical_mismatches: list[tuple[str, str, bool, bool]] = []
prompt_mismatches: list[tuple[str, str, bool, bool]] = []
with INPUT_RECORD.open("w", encoding="utf-8") as record:
    record.write("index\tcategory\tpython_repr\n")
    for index, (category, value) in enumerate(unique_cases):
        record.write(f"{index}\t{category}\t{value!r}\n")
        got = generated(value)
        canonical_value = canonical(value)
        prompt_value = prompt_oracle(value)
        if got != canonical_value:
            canonical_mismatches.append((category, value, got, canonical_value))
        if got != prompt_value:
            prompt_mismatches.append((category, value, got, prompt_value))

print(f"case_count={len(unique_cases)}")
print("generated_input_seed=124")
print(f"generated_input_alphabet={alphabet!r}")
print("generated_input_length_range=0..15")
print(f"generated_vs_prompt_mismatches={len(prompt_mismatches)}")
print(f"generated_vs_canonical_mismatches={len(canonical_mismatches)}")
print("first_generated_vs_canonical_mismatches:")
for category, value, got, expected in canonical_mismatches[:80]:
    print(
        f"  category={category} input={value!r} "
        f"generated={got!r} canonical={expected!r}"
    )
print("first_generated_vs_prompt_mismatches:")
for category, value, got, expected in prompt_mismatches[:80]:
    print(
        f"  category={category} input={value!r} "
        f"generated={got!r} prompt_oracle={expected!r}"
    )

assert not prompt_mismatches
print("DIFFERENTIAL_PROMPT_ORACLE=PASS")
