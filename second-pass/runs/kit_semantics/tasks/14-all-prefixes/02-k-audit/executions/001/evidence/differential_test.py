#!/usr/bin/env python3
"""Independent CPython differential test against the trusted canonical entry."""

from __future__ import annotations

import importlib.util
import random
import string
from pathlib import Path


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("/reference/canonical.py", "trusted_canonical")
candidate = load("/tmp/audit-work/solution.py", "generated_solution")

fixed_cases = [
    "",
    "a",
    "abc",  # documented example
    "ab",
    "abcd",
    "aa",
    "a a",
    " ",
    "\n",
    "!?",
    "0123456789",
    "é",
    "😀",
    "a😀b",
    "\x00",
    "prefix" * 20,
]

rng = random.Random(140014)
alphabet = string.ascii_letters + string.digits + " !?é😀"
generated_cases = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 65)))
    for _ in range(500)
]
cases = fixed_cases + generated_cases

mismatches = []
for value in cases:
    expected = canonical.all_prefixes(value)
    actual = candidate.all_prefixes(value)
    direct_contract = [value[:end] for end in range(1, len(value) + 1)]
    if actual != expected or expected != direct_contract:
        mismatches.append((value, expected, actual, direct_contract))

print(f"fixed_cases={len(fixed_cases)}")
print(f"generated_seed=140014 generated_cases={len(generated_cases)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(repr(mismatch))
    raise SystemExit(1)
