#!/usr/bin/env python3
"""Ground witnesses for each entry-domain/result branch."""

import importlib.util
import math
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_witness", "/reference/canonical.py").intersection
candidate = load("candidate_witness", "/candidate/solution.py").intersection


def formal_overlap(a0: int, a1: int, b0: int, b1: int) -> int:
    return (b1 if b1 < a1 else a1) - (b0 if b0 > a0 else a0)


def formal_prime_result(length: int) -> str:
    if length < 2:
        return "NO"
    has_divisor = any(length % divisor == 0 for divisor in range(2, length))
    return "NO" if has_divisor else "YES"


witnesses = [
    ("prime", 0, 2, 0, 2),
    ("length_three_prime", 10, 13, 0, 20),
    ("composite", 0, 4, 0, 4),
    ("length_one", 0, 1, 0, 1),
    ("disjoint", 0, 1, 3, 4),
    ("negative_coordinates", -101, -4, -200, 100),
]

for name, a0, a1, b0, b1 in witnesses:
    assert a0 <= a1 and b0 <= b1
    length = formal_overlap(a0, a1, b0, b1)
    claimed = formal_prime_result(length)
    trusted = canonical((a0, a1), (b0, b1))
    generated = candidate((a0, a1), (b0, b1))
    assert claimed == trusted == generated
    print(
        f"witness={name} inputs=(({a0},{a1}),({b0},{b1})) "
        f"precondition=true overlapLength={length} "
        f"primeResult={claimed} canonical={trusted} candidate={generated}"
    )

print(f"witness_count={len(witnesses)}")
print("all_claim_substitutions_match=true")
