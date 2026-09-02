#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs submitted solution."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.odd_count


if len(sys.argv) != 4:
    raise SystemExit(
        "usage: differential_test.py CANONICAL.py SOLUTION.py INPUTS.json"
    )

canonical = load_function("trusted_canonical", Path(sys.argv[1]))
submitted = load_function("submitted_solution", Path(sys.argv[2]))
inputs_path = Path(sys.argv[3])

cases: list[list[str]] = [
    [],
    [""],
    ["0"],
    ["1"],
    ["2"],
    ["9"],
    ["01"],
    ["10"],
    ["13579"],
    ["02468"],
    ["1234567"],
    ["3", "11111111"],
    ["", "0", "1", "2468", "13579"],
    ["1" * 9],
    ["1" * 10],
    ["1" * 11],
    ["0" * 20 + "1" * 20],
    ["9876543210" * 100],
]

# Exhaust every single digit string through length four. This covers both
# membership branches at every loop position and all short loop boundaries.
for length in range(5):
    for digits in itertools.product("0123456789", repeat=length):
        cases.append(["".join(digits)])

# Exercise interactions among multiple list elements, including empty strings.
pair_basis = ["", "0", "1", "2", "9", "10", "01", "13579", "02468"]
for left in pair_basis:
    for right in pair_basis:
        cases.append([left, right])

# Deterministic broader sample across list and string lengths.
rng = random.Random(113)
for _ in range(2000):
    value = []
    for _ in range(rng.randrange(0, 9)):
        length = rng.randrange(0, 41)
        value.append("".join(rng.choice("0123456789") for _ in range(length)))
    cases.append(value)

inputs_bytes = (
    json.dumps(cases, ensure_ascii=True, separators=(",", ":")) + "\n"
).encode()
inputs_path.write_bytes(inputs_bytes)

mismatches = []
for index, case in enumerate(cases):
    expected = canonical(case)
    actual = submitted(case)
    if actual != expected:
        mismatches.append(
            {"index": index, "input": case, "canonical": expected, "submitted": actual}
        )
        if len(mismatches) >= 20:
            break

print(f"cases={len(cases)}")
print("explicit_cases=18")
print("exhaustive_single_strings=11111 (all digit strings length 0..4)")
print(f"pair_cases={len(pair_basis) ** 2}")
print("generated_cases=2000 seed=113 list_length=0..8 string_length=0..40")
print(f"inputs_sha256={hashlib.sha256(inputs_bytes).hexdigest()}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches, indent=2, sort_keys=True))
    raise SystemExit(1)
print("DIFFERENTIAL=PASS")
