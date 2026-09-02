#!/usr/bin/env python3
"""Differential check: trusted HumanEval oracle versus submitted Python entry point."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


canonical = load_function("trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py"))
generated = load_function("generated_solution", Path("/tmp/audit-work/candidate-src/solution.py"))

documented = ["hi", "asdfghjkl", "gf", "et"]
boundaries = [
    "",
    "a",
    "v",
    "w",
    "x",
    "y",
    "z",
    "abcdefghijklmnopqrstuvwxyz",
    "A",
    "Z",
    "0",
    "9",
    " ",
    "!",
    "é",
    "🙂",
    "aA",
    "z!",
    "\n",
]
alphabet = ["a", "v", "w", "z", "A", "0", " "]
exhaustive_small = [
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(alphabet, repeat=length)
]
random.seed(890026)
pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !?"
generated_cases = [
    "".join(random.choice(pool) for _ in range(random.randrange(0, 33)))
    for _ in range(300)
]
long_boundary = ["a" * 1200]

groups = [
    ("documented", documented),
    ("boundaries", boundaries),
    ("exhaustive_small", exhaustive_small),
    ("generated", generated_cases),
    ("long_boundary", long_boundary),
]

mismatches = []
total = 0
for group, cases in groups:
    group_mismatches = 0
    group_errors = 0
    for value in cases:
        total += 1
        try:
            expected = canonical(value)
            expected_status = ("value", expected)
        except Exception as err:  # pragma: no cover - diagnostic path
            expected_status = ("error", type(err).__name__, str(err))
        try:
            actual = generated(value)
            actual_status = ("value", actual)
        except Exception as err:
            actual_status = ("error", type(err).__name__, str(err))
            group_errors += 1
        if actual_status != expected_status:
            group_mismatches += 1
            mismatches.append((group, value, expected_status, actual_status))
    print(
        f"GROUP {group} cases={len(cases)} "
        f"mismatches={group_mismatches} generated_errors={group_errors}"
    )

print(f"TOTAL cases={total} mismatches={len(mismatches)}")
for index, (group, value, expected, actual) in enumerate(mismatches[:20], 1):
    shown = repr(value if len(value) <= 80 else value[:77] + "...")
    print(
        f"MISMATCH {index} group={group} input={shown} "
        f"canonical={expected!r} generated={actual!r}"
    )

print("DOCUMENTED_EXAMPLES_MATCH", all(
    canonical(value) == generated(value) for value in documented
))
print("LOWERCASE_BOUNDARIES_MATCH", all(
    canonical(value) == generated(value)
    for value in ["", "a", "v", "w", "x", "y", "z", "abcdefghijklmnopqrstuvwxyz"]
))
print("INTENDED_DOMAIN_ALL_PYTHON_STRINGS")
sys.exit(0)
