#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from collections import Counter
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/124-valid-date")


def import_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = import_path("trusted_canonical", ROOT / "canonical.py")
candidate = import_path("candidate_solution", ROOT / "candidate" / "solution.py")


def oracle(value: str) -> bool:
    return canonical.valid_date(value)


def generated(value: str) -> bool:
    return candidate.valid_date(value)


cases: list[tuple[str, str]] = []


def add(category: str, *values: str) -> None:
    cases.extend((category, value) for value in values)


# Prompt examples.
add(
    "prompt-example",
    "03-11-2000",
    "15-01-2012",
    "04-0-2040",
    "06-04-2020",
    "06/04/2020",
)

# Empty, size, separator, character-class, and year-boundary cases.
add(
    "format-boundary",
    "",
    "-",
    "03-11-200",
    "03-11-20000",
    "003-11-2000",
    "03-011-2000",
    "03-11-0000",
    "03-11-9999",
    "03/11/2000",
    "03_11_2000",
    "aa-bb-cccc",
    "03-1a-2000",
    "03-11-20x0",
)

# Every material calendar branch boundary.
for month, days in [
    (0, [0, 1, 29, 30, 31, 32]),
    (1, [0, 1, 30, 31, 32]),
    (2, [0, 1, 28, 29, 30]),
    (3, [0, 1, 30, 31, 32]),
    (4, [0, 1, 29, 30, 31]),
    (6, [0, 1, 29, 30, 31]),
    (9, [0, 1, 29, 30, 31]),
    (11, [0, 1, 29, 30, 31]),
    (12, [0, 1, 30, 31, 32]),
    (13, [0, 1, 29, 30, 31]),
]:
    add(
        "calendar-boundary",
        *(f"{month:02d}-{day:02d}-2020" for day in days),
    )

# Exhaustive formatted grid around all branch bounds.
for month, day, year in itertools.product(range(0, 14), range(0, 33), [0, 1, 2020, 9999]):
    add("formatted-grid", f"{month:02d}-{day:02d}-{year:04d}")

# Inputs accepted by the trusted canonical parser but rejected by an exact-width
# parser. These are important differential witnesses, not an assertion that the
# prose necessarily intended every canonical tolerance.
add(
    "canonical-tolerance",
    "3-1-2000",
    "03-1-2000",
    "3-01-2000",
    " 03-11-2000",
    "03-11-2000 ",
    "\t03-11-2000\n",
    "+3-+1-+2000",
    "03-11-+2000",
    "003-011-02000",
)

# CPython str.isdigit/int support Unicode decimal digits. Arabic-Indic and
# full-width cases distinguish that behavior from an ASCII-only abstraction.
add(
    "unicode-decimal",
    "٠٣-١١-٢٠٠٠",
    "۰۳-۱۱-۲۰۰۰",
    "０３-１１-２０００",
    "٠٢-٢٩-٢٠٢٠",
    "١٣-٠١-٢٠٢٠",
)

# Deterministic representative malformed-string generation.
randomizer = random.Random(124)
alphabet = "0123456789-/x _"
for _ in range(1000):
    size = randomizer.randrange(0, 15)
    add(
        "seeded-malformed",
        "".join(randomizer.choice(alphabet) for _ in range(size)),
    )

category_counts = Counter(category for category, _ in cases)
mismatches: list[tuple[str, str, bool, bool]] = []
exceptions: list[tuple[str, str, str, str]] = []
for category, value in cases:
    try:
        expected = oracle(value)
        actual = generated(value)
    except Exception as error:  # Any unexpected exception remains visible.
        exceptions.append((category, repr(value), type(error).__name__, str(error)))
        continue
    if actual != expected:
        mismatches.append((category, value, expected, actual))

print("ORACLE=/tmp/audit-work/124-valid-date/canonical.py:valid_date")
print("CANDIDATE=/tmp/audit-work/124-valid-date/candidate/solution.py:valid_date")
print("RANDOM_SEED=124")
print(f"TOTAL_CASES={len(cases)}")
print("CATEGORY_COUNTS=" + repr(dict(sorted(category_counts.items()))))
print(f"EXCEPTIONS={len(exceptions)}")
for item in exceptions[:20]:
    print("EXCEPTION=" + repr(item))
print(f"MISMATCHES={len(mismatches)}")
print("MISMATCH_CATEGORIES=" + repr(dict(sorted(Counter(m[0] for m in mismatches).items()))))
for category, value, expected, actual in mismatches[:50]:
    print(
        f"MISMATCH category={category} input={value!r} "
        f"canonical={expected!r} candidate={actual!r}"
    )

# A differential mismatch is an audit result, not a script execution failure.
raise SystemExit(0 if not exceptions else 2)
