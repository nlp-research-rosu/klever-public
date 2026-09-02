#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/19."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/review-19/trusted/canonical.py")
)
generated = load_entry(
    "generated_solution", Path("/tmp/audit-work/review-19/candidate/solution.py")
)

words = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

categorized_cases: list[tuple[str, str]] = [
    ("documented-example", "three one five"),
    ("empty", ""),
    ("ascending", " ".join(words)),
    ("descending", " ".join(reversed(words))),
    ("leading-space", "  three one five"),
    ("trailing-space", "three one five  "),
    ("repeated-space", "three   one  five"),
    ("all-equal", "nine nine nine nine"),
]
categorized_cases.extend(("singleton-branch", word) for word in words)
categorized_cases.extend(
    ("double-branch", f"{left} {right}") for left in words for right in words
)
categorized_cases.extend(
    ("duplicate-boundary", f"{word} zero {word} nine {word}") for word in words
)

rng = random.Random(190019)
for length in list(range(0, 33)) + [50, 100, 256]:
    for _ in range(12):
        sequence = [rng.choice(words) for _ in range(length)]
        categorized_cases.append(("generated", " ".join(sequence)))

# Deduplicate while preserving the first category, so every executed input is explicit
# and the count/hash below is stable.
seen: set[str] = set()
cases: list[tuple[str, str]] = []
for category, case in categorized_cases:
    if case not in seen:
        seen.add(case)
        cases.append((category, case))

serialized = json.dumps(cases, ensure_ascii=True, separators=(",", ":")).encode()
print(f"CASE_COUNT: {len(cases)}")
print(f"CASES_JSON_SHA256: {hashlib.sha256(serialized).hexdigest()}")
category_counts: dict[str, int] = {}
for category, _ in cases:
    category_counts[category] = category_counts.get(category, 0) + 1
print(f"CATEGORY_COUNTS: {json.dumps(category_counts, sort_keys=True)}")

mismatches: list[tuple[str, str, object, object]] = []
for category, case in cases:
    try:
        expected: object = ("return", canonical(case))
    except Exception as error:  # Explicitly compare exception type if one arises.
        expected = ("raise", type(error).__name__)
    try:
        actual: object = ("return", generated(case))
    except Exception as error:
        actual = ("raise", type(error).__name__)
    if actual != expected:
        mismatches.append((category, case, expected, actual))

print(f"MISMATCH_COUNT: {len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH: {mismatch!r}")
print(f"FIRST_CASES: {cases[:12]!r}")
print(f"LAST_CASES: {cases[-3:]!r}")
raise SystemExit(1 if mismatches else 0)
