#!/usr/bin/env python3
"""Independent differential test for HumanEval 113 over the ASCII-digit domain."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.odd_count


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_113")
generated = load_entry(Path("/tmp/audit-work/113-odd-count/solution.py"), "candidate_solution_113")


def independent_oracle(values: list[str]) -> list[str]:
    template = "the number of odd elements in the string i of the input."
    return [template.replace("i", str(sum(ch in "13579" for ch in value))) for value in values]


named_cases: list[tuple[str, list[str]]] = [
    ("documented-one", ["1234567"]),
    ("documented-two", ["3", "11111111"]),
    ("empty-list", []),
    ("empty-string", [""]),
    ("all-single-digits", list("0123456789")),
    ("even-only", ["02468", "0000", "2468024680"]),
    ("odd-only", ["13579", "11111111111"]),
    ("leading-zero-and-mixed", ["000123", "9081726354"]),
    ("repeated-elements", ["7", "7", "", "20", "20"]),
    ("multi-digit-count", ["1" * 12, "0" * 12]),
    ("long-string", [("0123456789" * 200)]),
]

cases: list[tuple[str, list[str]]] = list(named_cases)
for length in range(5):
    for chars in itertools.product("0123456789", repeat=length):
        value = "".join(chars)
        cases.append((f"exhaustive-single-len-{length}", [value]))

small_values = ["", "0", "1", "2", "9", "10", "135", "246", "9090"]
for width in range(4):
    for values in itertools.product(small_values, repeat=width):
        cases.append((f"cartesian-list-width-{width}", list(values)))

rng = random.Random(113_20260722)
for index in range(2000):
    values = [
        "".join(rng.choice("0123456789") for _ in range(rng.randrange(0, 31)))
        for _ in range(rng.randrange(0, 9))
    ]
    cases.append((f"generated-{index}", values))

mismatches: list[tuple[str, list[str], object, object, object]] = []
for label, values in cases:
    expected = independent_oracle(values)
    canonical_result = canonical(values)
    generated_result = generated(values)
    if canonical_result != expected or generated_result != expected:
        mismatches.append((label, values, expected, canonical_result, generated_result))

print(f"named_cases={len(named_cases)}")
print("exhaustive_single_strings=11111 (all lengths 0..4 over ASCII 0..9)")
print("cartesian_lists=820 (widths 0..3 over 9 boundary strings)")
print("deterministic_generated_lists=2000 (seed 113_20260722)")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:10]:
    print(repr(mismatch))
raise SystemExit(1 if mismatches else 0)
