#!/usr/bin/env python3
"""Independent differential test for trusted and submitted Python entry points."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType


TRUSTED = Path("/tmp/audit-work/27-flip-case/trusted/canonical.py")
SUBMITTED = Path("/tmp/audit-work/27-flip-case/candidate/solution.py")


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", TRUSTED)
generated = load("submitted_solution", SUBMITTED)

mismatches: list[dict[str, str]] = []
category_counts: dict[str, int] = {}


def check(category: str, value: str) -> None:
    category_counts[category] = category_counts.get(category, 0) + 1
    expected = canonical.flip_case(value)
    actual = generated.flip_case(value)
    if actual != expected and len(mismatches) < 20:
        mismatches.append(
            {
                "category": category,
                "input": repr(value),
                "canonical": repr(expected),
                "submitted": repr(actual),
            }
        )


# Contract example plus empty/boundary values around the ASCII case ranges.
documented = [("Hello", "hELLO")]
for value, expected in documented:
    check("documented", value)
    actual = generated.flip_case(value)
    if actual != expected:
        mismatches.append(
            {
                "category": "documented_expected",
                "input": repr(value),
                "canonical": repr(expected),
                "submitted": repr(actual),
            }
        )

curated = [
    "",
    "@AZ[",
    "`az{",
    "A",
    "Z",
    "a",
    "z",
    "0 9!_",
    "Python 3.11",
    "\x00A\x7fz",
    "éÉ",
    "ßẞ",
    "Σσς",
    "İı",
    "ǅǄǆ",
    "a\u0301A\u0301",
    "🙂A🙂z",
]
for value in curated:
    check("curated_boundaries", value)

# Exhaustive short combinations hit lower, upper, digit, punctuation, NUL, and
# non-ASCII paths together rather than only in isolation.
alphabet = ("A", "Z", "a", "z", "0", "@", "{", "\x00", "ß")
for length in range(5):
    for chars in itertools.product(alphabet, repeat=length):
        check("exhaustive_short", "".join(chars))

# Every possible Python code point as a one-character string, including the
# surrogate code points Python permits internally.
for code_point in range(0x110000):
    check("all_single_codepoints", chr(code_point))

# Deterministic broader strings exercise interactions and multi-code-point
# expansions such as the swapcase of sharp s.
rng = random.Random(270027)
for _ in range(2000):
    length = rng.randrange(0, 65)
    value = "".join(chr(rng.randrange(0x110000)) for _ in range(length))
    check("deterministic_generated", value)

result = {
    "oracle": str(TRUSTED),
    "submitted": str(SUBMITTED),
    "categories": category_counts,
    "total_comparisons": sum(category_counts.values()),
    "mismatch_count": len(mismatches),
    "first_mismatches": mismatches,
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True))
raise SystemExit(1 if mismatches else 0)
