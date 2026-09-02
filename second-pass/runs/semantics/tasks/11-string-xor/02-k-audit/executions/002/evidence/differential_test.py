#!/usr/bin/env python3
"""Independent differential checks for HumanEval 11 string_xor."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


canonical = load_function(
    "trusted_canonical", Path("/tmp/audit-work/11-string-xor/trusted/canonical.py")
)
generated = load_function(
    "generated_solution", Path("/tmp/audit-work/11-string-xor/candidate/solution.py")
)


def independent_oracle(a: str, b: str) -> str:
    table = {
        ("0", "0"): "0",
        ("0", "1"): "1",
        ("1", "0"): "1",
        ("1", "1"): "0",
    }
    return "".join(table[pair] for pair in zip(a, b))


manual_cases = [
    ("010", "110"),  # documented example
    ("", ""),        # both empty
    ("", "0"),       # first empty
    ("1", ""),       # second empty
    ("0", "0"),      # equal-zero branch
    ("1", "1"),      # equal-one branch
    ("0", "1"),      # unequal 0/1 branch
    ("1", "0"),      # unequal 1/0 branch
    ("10", "1"),     # second shorter
    ("0", "11"),     # first shorter
    ("000000", "111111"),
    ("101010", "010101"),
]

all_strings = [""]
for length in range(1, 7):
    all_strings.extend("".join(bits) for bits in itertools.product("01", repeat=length))
exhaustive_cases = list(itertools.product(all_strings, repeat=2))

rng = random.Random(110011)
random_cases = []
for _ in range(2000):
    left_len = rng.randrange(0, 257)
    right_len = rng.randrange(0, 257)
    left = "".join(rng.choice("01") for _ in range(left_len))
    right = "".join(rng.choice("01") for _ in range(right_len))
    random_cases.append((left, right))

cases = manual_cases + exhaustive_cases + random_cases
encoded_cases = "\n".join(json.dumps(case) for case in cases).encode()
case_digest = hashlib.sha256(encoded_cases).hexdigest()

mismatches = []
for index, (a, b) in enumerate(cases):
    expected = independent_oracle(a, b)
    canonical_result = canonical(a, b)
    generated_result = generated(a, b)
    if canonical_result != expected or generated_result != expected:
        mismatches.append(
            {
                "index": index,
                "a": a,
                "b": b,
                "oracle": expected,
                "canonical": canonical_result,
                "generated": generated_result,
            }
        )
        if len(mismatches) >= 20:
            break

print(f"manual_cases={len(manual_cases)}")
print(f"exhaustive_binary_pairs_max_each_length=6 count={len(exhaustive_cases)}")
print(f"random_seed=110011 random_cases={len(random_cases)} max_length=256")
print(f"total_cases={len(cases)}")
print(f"case_sha256={case_digest}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches, indent=2))
    raise SystemExit(1)
print("DIFFERENTIAL_OK")
