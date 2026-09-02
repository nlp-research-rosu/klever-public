#!/usr/bin/env python3
"""Check the finite verification predicate against independent prime triples."""

from __future__ import annotations

import re
from pathlib import Path


text = Path("/candidate/verification.k").read_text()
factor_groups = re.findall(r"A\s*==Int\s*\(([^()]*)\)", text)
declared_values = []
for group in factor_groups:
    factors = [int(token) for token in re.findall(r"-?\d+", group)]
    value = 1
    for factor in factors:
        value *= factor
    declared_values.append(value)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % divisor for divisor in range(2, int(n**0.5) + 1))


primes = [value for value in range(2, 100) if is_prime(value)]
independent_values = sorted(
    {
        p * q * r
        for p in primes
        for q in primes
        for r in primes
        if p <= q <= r and p * q * r < 100
    }
)
declared_set = sorted(set(declared_values))

print("declared_factor_groups", factor_groups)
print("declared_values", declared_values)
print("declared_unique_values", declared_set)
print("independent_prime_triple_values", independent_values)
print("declared_count", len(declared_values))
print("declared_unique_count", len(declared_set))
print("independent_count", len(independent_values))
print("sets_equal", declared_set == independent_values)
print("no_duplicate_disjuncts", len(declared_values) == len(declared_set))

assert declared_set == independent_values
assert len(declared_values) == len(declared_set)
