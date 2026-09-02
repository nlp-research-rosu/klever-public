#!/usr/bin/env python3
"""Independent differential test for HumanEval 107."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def direct_oracle(n: int) -> tuple[int, int]:
    palindromes = [value for value in range(1, n + 1) if str(value) == str(value)[::-1]]
    return (
        sum(value % 2 == 0 for value in palindromes),
        sum(value % 2 == 1 for value in palindromes),
    )


canonical = load("/reference/canonical.py", "trusted_canonical")
generated = load("/candidate/solution.py", "generated_solution")

examples = {3: (1, 2), 12: (4, 6)}
explicit_cases = [
    0,  # empty range, outside but adjacent to the documented positive domain
    1,
    2,
    3,
    8,
    9,
    10,
    11,
    12,
    99,
    100,
    101,
    109,
    110,
    111,
    120,
    121,
    199,
    200,
    201,
    202,
    989,
    990,
    999,
    1000,
]
rng = random.Random(107)
generated_cases = [rng.randint(1, 1000) for _ in range(64)]
intended_domain = list(range(1, 1001))
all_cases = sorted(set(explicit_cases + generated_cases + intended_domain))

mismatches = []
records = []
for n in all_cases:
    expected = canonical.even_odd_palindrome(n)
    actual = generated.even_odd_palindrome(n)
    direct = direct_oracle(n)
    records.append((n, expected, actual, direct))
    if expected != actual or expected != direct:
        mismatches.append((n, expected, actual, direct))

for n, wanted in examples.items():
    assert canonical.even_odd_palindrome(n) == wanted
    assert generated.even_odd_palindrome(n) == wanted

digest = hashlib.sha256(
    json.dumps(records, separators=(",", ":")).encode()
).hexdigest()
print("COMMAND: python3 /audit-output/evidence/differential_test.py")
print("oracle=trusted canonical.py plus independent direct decimal-palindrome enumeration")
print("intended_domain=every integer 1..1000 inclusive")
print(f"empty_adjacent_case={[0]}")
print(f"explicit_boundary_cases={explicit_cases}")
print(f"deterministic_generated_seed=107 generated_draw_count={len(generated_cases)}")
print(f"deterministic_generated_inputs={generated_cases}")
print(f"unique_inputs_executed={len(all_cases)}")
print(f"result_record_sha256={digest}")
for n in explicit_cases:
    expected = canonical.even_odd_palindrome(n)
    actual = generated.even_odd_palindrome(n)
    direct = direct_oracle(n)
    print(f"case n={n} canonical={expected} generated={actual} direct={direct}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch}")
raise SystemExit(1 if mismatches else 0)
