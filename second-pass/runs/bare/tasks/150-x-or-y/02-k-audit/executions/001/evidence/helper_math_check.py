#!/usr/bin/env python3
"""Finite independent check of the proof helpers on their actual D >= 2 use domain."""
import math


def k_prime_from(n: int, d: int) -> bool:
    while True:
        if n < d * d:
            return True
        if n % d == 0:
            return False
        d += 1


def independent_prime_from(n: int, d: int) -> bool:
    upper = math.isqrt(n) if n >= 0 else -1
    return all(n % candidate != 0 for candidate in range(d, upper + 1))


def independent_is_prime(n: int) -> bool:
    return n >= 2 and independent_prime_from(n, 2)


mismatches = []
true_count = 0
false_count = 0
for n in range(-20, 501):
    for d in range(2, 31):
        helper = k_prime_from(n, d)
        oracle = independent_prime_from(n, d)
        true_count += int(helper)
        false_count += int(not helper)
        if helper != oracle:
            mismatches.append((n, d, helper, oracle))

is_prime_mismatches = [
    n
    for n in range(-20, 501)
    if (False if n < 2 else k_prime_from(n, 2)) != independent_is_prime(n)
]

print("primeFrom domain tested: N=-20..500, D=2..30")
print(f"cases={521 * 29} true_outcomes={true_count} false_outcomes={false_count}")
print(f"primeFrom_mismatches={len(mismatches)}")
print(f"isPrime_mismatches={len(is_prime_mismatches)}")
print("distinct witnesses: primeFrom(7,2)=true; primeFrom(9,3)=false")
raise SystemExit(1 if mismatches or is_prime_mismatches else 0)
