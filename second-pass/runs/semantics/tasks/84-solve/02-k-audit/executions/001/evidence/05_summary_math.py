#!/usr/bin/env python3
"""Independent finite check of proof summaries against decimal-string intent."""

from __future__ import annotations

import hashlib
import sys


def decimal_digit(n: int, place: int) -> int:
    if place == 1:
        return n % 10
    return ((n - (n % place)) // place) % 10


places = (1, 10, 100, 1000, 10000)
mismatches: list[tuple[int, int, int]] = []
rows: list[str] = []
for n in range(0, 10001):
    proof_sum = sum(decimal_digit(n, place) for place in places)
    oracle_sum = sum(int(character) for character in str(n))
    proof_result = bin(proof_sum)[2:]
    oracle_result = bin(oracle_sum)[2:]
    rows.append(f"{n}:{proof_sum}:{proof_result}\n")
    if proof_sum != oracle_sum or proof_result != oracle_result:
        mismatches.append((n, proof_sum, oracle_sum))

for witness in (0, 147, 150, 1000, 9999, 10000):
    digit_sum = sum(decimal_digit(witness, place) for place in places)
    print(f"witness N={witness}: digit_sum={digit_sum}, result={bin(digit_sum)[2:]}")
print(f"checked_inputs={len(rows)}")
print(f"mismatch_count={len(mismatches)}")
print(f"rows_sha256={hashlib.sha256(''.join(rows).encode()).hexdigest()}")
if mismatches:
    print(mismatches[:50])
    sys.exit(1)
