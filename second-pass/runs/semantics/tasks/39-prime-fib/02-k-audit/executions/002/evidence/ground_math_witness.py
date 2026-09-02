#!/usr/bin/env python3
"""Independent arithmetic witnesses for the eleven ground postconditions."""

from __future__ import annotations

import math

claimed = [
    2,
    3,
    5,
    13,
    89,
    233,
    1597,
    28657,
    514229,
    433494437,
    2971215073,
]
cached_false = [17711, 121393, 1346269, 5702887, 165580141, 1836311903]


def smallest_factor(value: int) -> int | None:
    if value < 2:
        return None
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return divisor
    return value


fibonacci_primes = []
first, second = 0, 1
index = 0
while len(fibonacci_primes) < len(claimed):
    value = first
    factor = smallest_factor(value)
    if factor == value and value >= 2:
        fibonacci_primes.append((len(fibonacci_primes) + 1, index, value))
    first, second = second, first + second
    index += 1

print("GROUND FIBONACCI PRIME TABLE")
for ordinal, fib_index, value in fibonacci_primes:
    print(
        f"ordinal={ordinal} fibonacci_index={fib_index} value={value} "
        f"trial_division_limit={math.isqrt(value)}"
    )
print(f"claimed_values_match={claimed == [row[2] for row in fibonacci_primes]}")

print("CACHED FALSE FACTORIZATIONS")
for value in cached_false:
    factor = smallest_factor(value)
    assert factor is not None and factor != value
    print(f"value={value} factorization={factor}*{value // factor}")

raise SystemExit(0 if claimed == [row[2] for row in fibonacci_primes] else 1)
