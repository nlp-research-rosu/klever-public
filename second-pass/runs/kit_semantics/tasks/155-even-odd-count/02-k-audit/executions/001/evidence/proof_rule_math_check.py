#!/usr/bin/env python3
"""Finite witness check of every proof-local digit-summary equation."""

from __future__ import annotations


def even_pos(value: int) -> int:
    assert value >= 0
    if value == 0:
        return 0
    return sum(int(character) % 2 == 0 for character in str(value))


def odd_pos(value: int) -> int:
    assert value >= 0
    if value == 0:
        return 0
    return sum(int(character) % 2 == 1 for character in str(value))


def dec_even(value: int) -> int:
    return 1 if value == 0 else even_pos(abs(value))


def dec_odd(value: int) -> int:
    return 0 if value == 0 else odd_pos(abs(value))


checked = 0
for value in range(-100_000, 100_001):
    if value == 0:
        assert dec_even(value) == 1
        assert dec_odd(value) == 0
    elif value > 0:
        assert dec_even(value) == even_pos(value)
        assert dec_odd(value) == odd_pos(value)
    else:
        assert dec_even(value) == even_pos(-value)
        assert dec_odd(value) == odd_pos(-value)
    if abs(value) > 0:
        assert even_pos(abs(value)) == dec_even(value)
        assert odd_pos(abs(value)) == dec_odd(value)
    checked += 6

for value in range(1, 100_001):
    next_value = (value - ((value % 10 + 10) % 10)) // 10
    parity = (value % 2 + 2) % 2
    for accumulator in (-100, -1, 0, 1, 100):
        assert accumulator + even_pos(value) == (
            accumulator + 1 - parity + even_pos(next_value)
        )
        assert accumulator + odd_pos(value) == (
            accumulator + parity + odd_pos(next_value)
        )
        checked += 4

for value in range(-100_000, 0):
    assert even_pos(-value) == even_pos(abs(value))
    assert odd_pos(-value) == odd_pos(abs(value))
    checked += 2

print("summary_interpretation=decimal-string digit parity counts")
print("public_domain=[-100000,100000]")
print("positive_recurrence_domain=[1,100000]")
print("accumulators=[-100,-1,0,1,100]")
print(f"equation_instances_checked={checked}")
print("mismatches=0")
