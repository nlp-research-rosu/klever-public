#!/usr/bin/env python3
"""Finite boundary checks supporting, but not proving, the K classification audit."""

from itertools import product
from random import Random


def source_oracle(codes: tuple[int, ...]) -> tuple[int, ...]:
    output: list[int] = []
    for code in codes:
        if code >= 97 and code <= 122:
            output.append((code - 97 + 4) % 26 + 97)
        else:
            output.append(code)
    return tuple(output)


def rot4_code(code: int) -> int:
    return ((code - 97 + 4) % 26) + 97


def encrypted_char(code: int) -> tuple[int, ...]:
    if code < 97:
        return (code,)
    if code <= 122:
        return (rot4_code(code),)
    return (code,)


def encrypt_fold(accumulator: tuple[int, ...], rest: tuple[int, ...]) -> tuple[int, ...]:
    if not rest:
        return accumulator
    return encrypt_fold(accumulator + encrypted_char(rest[0]), rest[1:])


def final_loop_char(rest: tuple[int, ...], initial: tuple[int, ...]) -> tuple[int, ...]:
    if not rest:
        return initial
    return final_loop_char(rest[1:], (rest[0],))


fixed = [(), (96,), (97,), (118,), (119,), (122,), (123,), (97, 33, 122)]
exhaustive = [value for length in range(3) for value in product(range(128), repeat=length)]
rng = Random(8904)
sampled = [tuple(rng.randrange(128) for _ in range(rng.randrange(11))) for _ in range(1000)]
cases = fixed + exhaustive + sampled
mismatches = [
    (case, source_oracle(case), encrypt_fold((), case))
    for case in cases
    if source_oracle(case) != encrypt_fold((), case)
]

print(f"cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for case in fixed:
    print(
        f"boundary input={case} output={encrypt_fold((), case)} "
        f"final={final_loop_char(case, ())}"
    )

counterfactuals = {
    "identity rotation": ((97,), source_oracle((97,)), (97,)),
    "constant rotation": ((98,), source_oracle((98,)), (101,)),
    "no wraparound": ((122,), source_oracle((122,)), (126,)),
    "reversed fold": ((97, 98), source_oracle((97, 98)), (102, 101)),
    "widened lowercase guard": ((123,), source_oracle((123,)), (101,)),
    "constant final loop target": ((97,), final_loop_char((97,), ()), ()),
}
for name, (case, expected, mutated) in counterfactuals.items():
    assert expected != mutated
    print(f"counterfactual={name!r} input={case} expected={expected} mutated={mutated} rejected")

assert not mismatches
