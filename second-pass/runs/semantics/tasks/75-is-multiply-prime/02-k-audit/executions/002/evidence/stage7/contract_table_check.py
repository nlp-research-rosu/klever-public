#!/usr/bin/env python3
"""Exhaustively connect the finite positive spec table to the prime-product contract."""

from __future__ import annotations

import re
from pathlib import Path


def is_prime_by_definition(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor != 0 for divisor in range(2, value))


primes = [value for value in range(2, 100) if is_prime_by_definition(value)]
triple_products_below_100 = {
    first * second * third
    for first in primes
    for second in primes
    for third in primes
    if first * second * third < 100
}

spec = Path("/tmp/audit-work/75-is-multiply-prime/spec.k").read_text()
pairs = {
    int(number): expected == "true"
    for number, expected in re.findall(
        r"#runIsMultiplyPrime\((\d+)\)\s*~>\s*#expect\((true|false)\)",
        spec,
    )
}

expected_domain = set(range(2, 100))
table_true = {number for number, expected in pairs.items() if expected}
mismatches = [
    number
    for number in range(2, 100)
    if pairs.get(number) != (number in triple_products_below_100)
]

print(f"primes_2_through_99={primes}")
print(f"three_prime_products_below_100={sorted(triple_products_below_100)}")
print(f"spec_true_inputs={sorted(table_true)}")
print(f"spec_domain_exact={set(pairs) == expected_domain}")
print(f"prime_product_table_mismatch_count={len(mismatches)}")
print(f"prime_product_table_mismatches={mismatches}")
print(
    "negative_domain_argument: every prime in the definition is >=2, so every "
    "product of three primes is >=8; therefore every integer A<2 must return false"
)

okay = (
    set(pairs) == expected_domain
    and table_true == triple_products_below_100
    and not mismatches
)
raise SystemExit(0 if okay else 1)
