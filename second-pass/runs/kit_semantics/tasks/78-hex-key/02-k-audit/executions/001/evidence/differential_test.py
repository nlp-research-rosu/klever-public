#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 78 (hex_key)."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


def independent_oracle(value: str) -> int:
    prime_digits = frozenset(("2", "3", "5", "7", "B", "D"))
    total = 0
    for character in value:
        if character in prime_digits:
            total += 1
    return total


if len(sys.argv) != 3:
    raise SystemExit("usage: differential_test.py CANONICAL.py SOLUTION.py")

canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
generated = load_entry(Path(sys.argv[2]), "generated_solution")

documented = {
    "AB": 1,
    "1077E": 2,
    "ABED1A33": 4,
    "123456789ABCDEF0": 6,
    "2020": 2,
}
alphabet = "0123456789ABCDEF"

cases: list[tuple[str, str]] = []
cases.append(("empty", ""))
for value, expected in documented.items():
    cases.append((f"documented(expected={expected})", value))
for character in alphabet:
    cases.append(("single-character-branch", character))
for value in (
    "2357BD",
    "014689ACEF",
    "22222222",
    "00000000",
    "DDDDDDDD",
    "FFFFFFFF",
    "20" * 64,
    "0123456789ABCDEF" * 16,
):
    cases.append(("boundary-pattern", value))

for length in range(5):
    for symbols in itertools.product(alphabet, repeat=length):
        cases.append((f"exhaustive-length-{length}", "".join(symbols)))

rng = random.Random(0x78A11D)
for index in range(1000):
    length = rng.randrange(0, 257)
    value = "".join(rng.choice(alphabet) for _ in range(length))
    cases.append((f"deterministic-random-{index}", value))

mismatches: list[tuple[str, str, int, int, int]] = []
for category, value in cases:
    trusted_result = canonical(value)
    generated_result = generated(value)
    oracle_result = independent_oracle(value)
    expected = documented.get(value)
    if (
        trusted_result != generated_result
        or generated_result != oracle_result
        or (expected is not None and generated_result != expected)
    ):
        mismatches.append(
            (
                category,
                value,
                trusted_result,
                generated_result,
                oracle_result,
            )
        )
        if len(mismatches) >= 20:
            break

print(f"documented_cases={len(documented)}")
print("branch_singletons=16 (true branch: 2,3,5,7,B,D; false branch: other 10)")
print("exhaustive_domain=all uppercase hexadecimal strings of lengths 0..4")
print("generated_domain=1000 deterministic strings of lengths 0..256")
print(f"total_comparisons={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch!r}")

if mismatches:
    raise SystemExit(1)
