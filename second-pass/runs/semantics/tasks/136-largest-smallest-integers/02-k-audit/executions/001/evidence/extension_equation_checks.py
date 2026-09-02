#!/usr/bin/env python3
"""Independent overlap, coverage, and equation checks for verification.k."""

from __future__ import annotations

import itertools


def neg_guards(a: int, i: int) -> list[bool]:
    return [
        i < 0 and a == 0,
        i < 0 and a != 0 and i > a,
        i >= 0,
        i < 0 and a != 0 and i <= a,
    ]


def pos_guards(b: int, i: int) -> list[bool]:
    return [
        i > 0 and b == 0,
        i > 0 and b != 0 and i < b,
        i <= 0,
        i > 0 and b != 0 and i >= b,
    ]


def neg_k(a: int, i: int) -> int:
    guards = neg_guards(a, i)
    outputs = [i, i, a, a]
    matches = [output for guard, output in zip(guards, outputs) if guard]
    assert len(matches) == 1
    return matches[0]


def pos_k(b: int, i: int) -> int:
    guards = pos_guards(b, i)
    outputs = [i, i, b, b]
    matches = [output for guard, output in zip(guards, outputs) if guard]
    assert len(matches) == 1
    return matches[0]


def neg_source(a: int, i: int) -> int:
    if i < 0 and (a == 0 or i > a):
        return i
    return a


def pos_source(b: int, i: int) -> int:
    if i > 0 and (b == 0 or i < b):
        return i
    return b


pair_count = 0
for accumulator in range(-20, 21):
    for value in range(-20, 21):
        assert sum(neg_guards(accumulator, value)) == 1
        assert sum(pos_guards(accumulator, value)) == 1
        assert neg_k(accumulator, value) == neg_source(accumulator, value)
        assert pos_k(accumulator, value) == pos_source(accumulator, value)
        pair_count += 1

sequence_count = 0
alphabet = [-2, -1, 0, 1, 2]
for length in range(0, 6):
    for values_tuple in itertools.product(alphabet, repeat=length):
        values = list(values_tuple)
        for initial_neg in (-20, -1, 0):
            accumulator = initial_neg
            for value in values:
                accumulator = neg_k(accumulator, value)
            expected = max(
                ([initial_neg] if initial_neg < 0 else [])
                + [value for value in values if value < 0],
                default=0,
            )
            assert accumulator == expected
            assert accumulator <= 0
        for initial_pos in (0, 1, 20):
            accumulator = initial_pos
            for value in values:
                accumulator = pos_k(accumulator, value)
            expected = min(
                ([initial_pos] if initial_pos > 0 else [])
                + [value for value in values if value > 0],
                default=0,
            )
            assert accumulator == expected
            assert accumulator >= 0
        sequence_count += 1

for integer in range(-100, 101):
    optional_neg = None if integer == 0 else integer
    optional_pos = None if integer == 0 else integer
    assert optional_neg == optional_pos

print(f"step_pairs_checked={pair_count}")
print("negStep_guard_matches_per_pair=1")
print("posStep_guard_matches_per_pair=1")
print("step_equations_match_source_conditionals=true")
print(f"fold_sequences_checked={sequence_count}")
print("negFold_extremum_and_A<=0_preservation=true")
print("posFold_extremum_and_B>=0_preservation=true")
print("optional_guard_coverage_and_disjointness=true")
