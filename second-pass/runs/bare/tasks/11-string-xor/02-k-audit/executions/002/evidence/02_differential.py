#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/11."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/11-string-xor/reference/canonical.py")
)
candidate = load_entry(
    "candidate_solution", Path("/tmp/audit-work/11-string-xor/source/solution.py")
)

documented_and_boundary = [
    ("010", "110"),
    ("", ""),
    ("", "0"),
    ("1", ""),
    ("0", "0"),
    ("1", "1"),
    ("0", "1"),
    ("1", "0"),
    ("00", "00"),
    ("01", "10"),
    ("0101", "11"),
    ("11", "0101"),
    ("0" * 900, "1" * 900),
]

checked = 0
for a, b in documented_and_boundary:
    expected = canonical(a, b)
    actual = candidate(a, b)
    assert actual == expected, (a, b, expected, actual)
    checked += 1

# Exhaust all pairs whose respective lengths range independently over 0..7.
all_small = [
    "".join(bits)
    for length in range(8)
    for bits in itertools.product("01", repeat=length)
]
for a in all_small:
    for b in all_small:
        expected = canonical(a, b)
        actual = candidate(a, b)
        assert actual == expected, (a, b, expected, actual)
        checked += 1

# Deterministic representative coverage at larger and unequal lengths.
rng = random.Random(110011)
for _ in range(2000):
    length_a = rng.randrange(0, 121)
    length_b = rng.randrange(0, 121)
    a = "".join(rng.choice("01") for _ in range(length_a))
    b = "".join(rng.choice("01") for _ in range(length_b))
    expected = canonical(a, b)
    actual = candidate(a, b)
    assert actual == expected, (a, b, expected, actual)
    checked += 1

print(f"documented_boundary_cases={len(documented_and_boundary)}")
print(f"exhaustive_strings={len(all_small)}")
print(f"exhaustive_pairs={len(all_small) ** 2}")
print("random_seed=110011")
print("random_pairs=2000")
print(f"total_pairs={checked}")
print("mismatches=0")
