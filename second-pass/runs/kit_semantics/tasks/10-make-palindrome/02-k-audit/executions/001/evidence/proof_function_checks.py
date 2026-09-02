#!/usr/bin/env python3
"""Independent executable checks of every proof-local mathematical equation."""

from __future__ import annotations

import itertools
import random


Seq = tuple[int, ...]


def reverse_acc(remaining: Seq, accumulator: Seq) -> Seq:
    if not remaining:
        return accumulator
    return reverse_acc(remaining[1:], (remaining[0],) + accumulator)


def pal_is(value: Seq) -> bool:
    return value == reverse_acc(value, ())


def seed_result(value: Seq) -> Seq:
    return value if pal_is(value) else value + reverse_acc(value, ())


def search_result(
    original: Seq,
    remaining: Seq,
    prefix: Seq,
    reverse_prefix: Seq,
    reverse_original: Seq,
    found: bool,
    result: Seq,
) -> Seq:
    if found:
        return result
    if not remaining:
        return result
    char, rest = remaining[0], remaining[1:]
    next_prefix = prefix + (char,)
    next_reverse_prefix = (char,) + reverse_prefix
    candidate = original + next_reverse_prefix
    if next_prefix + reverse_original == candidate:
        return candidate
    return search_result(
        original,
        rest,
        next_prefix,
        next_reverse_prefix,
        reverse_original,
        False,
        result,
    )


def execute_search_loop(
    original: Seq,
    remaining: Seq,
    prefix: Seq,
    reverse_prefix: Seq,
    reverse_original: Seq,
    found: bool,
    result: Seq,
) -> Seq:
    for char in remaining:
        if not found:
            prefix = prefix + (char,)
            reverse_prefix = (char,) + reverse_prefix
            if original + reverse_prefix == prefix + reverse_original:
                result = original + reverse_prefix
                found = True
    return result


def complete_pal(value: Seq) -> Seq:
    return search_result(
        value,
        value,
        (),
        (),
        reverse_acc(value, ()),
        pal_is(value),
        seed_result(value),
    )


def shortest_oracle(value: Seq) -> Seq:
    for size in range(len(value) + 1):
        candidate = value + tuple(reversed(value[:size]))
        if candidate == tuple(reversed(candidate)):
            return candidate
    raise AssertionError


alphabet = (0, 1, 2)
sequences = [
    tuple(items)
    for length in range(8)
    for items in itertools.product(alphabet, repeat=length)
]
for value in sequences:
    assert reverse_acc(value, ()) == tuple(reversed(value))
    assert pal_is(value) == (value == tuple(reversed(value)))
    assert seed_result(value) == (
        value if value == tuple(reversed(value)) else value + tuple(reversed(value))
    )
    assert complete_pal(value) == shortest_oracle(value)

rng = random.Random(0x510A7)
search_cases = 25_000
base_true_empty_overlap = 0
for _ in range(search_cases):
    def random_seq(max_length: int = 8) -> Seq:
        return tuple(rng.randrange(-2, 5) for _ in range(rng.randrange(max_length + 1)))

    original = random_seq()
    remaining = random_seq()
    prefix = random_seq()
    reverse_prefix = random_seq()
    reverse_original = random_seq()
    found = bool(rng.randrange(2))
    result = random_seq()
    if found and not remaining:
        base_true_empty_overlap += 1
    summary = search_result(
        original,
        remaining,
        prefix,
        reverse_prefix,
        reverse_original,
        found,
        result,
    )
    execution = execute_search_loop(
        original,
        remaining,
        prefix,
        reverse_prefix,
        reverse_original,
        found,
        result,
    )
    assert summary == execution

print(f"exhaustive_sequences={len(sequences)} alphabet={alphabet} max_length=7")
print(f"arbitrary_search_states={search_cases}")
print(f"overlapping_true_empty_base_states={base_true_empty_overlap}")
print("mismatches=0")
