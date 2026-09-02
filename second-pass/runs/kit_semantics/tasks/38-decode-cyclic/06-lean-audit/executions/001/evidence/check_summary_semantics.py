#!/usr/bin/env python3
"""Finite adversarial checks supplementing the source/semantics induction audit."""

from itertools import product


def operational_decode(codes):
    result = []
    group = []
    final_char = ("old",)
    for char in codes:
        final_char = (char,)
        group = group + [char]
        if len(group) == 3:
            result = result + [group[2]] + group[:2]
            group = []
    return result + group, result, group, final_char


def decoded_result(acc, remaining):
    if len(remaining) < 3:
        return acc
    a, b, c, *rest = remaining
    return decoded_result(acc + [c, a, b], rest)


def decoded_tail(remaining):
    if len(remaining) < 3:
        return remaining
    return decoded_tail(remaining[3:])


def decode_codes(codes):
    return decoded_result([], codes) + decoded_tail(codes)


def final_loop_char(codes, old):
    if not codes:
        return old
    return final_loop_char(codes[1:], (codes[0],))


checked = 0
for length in range(10):
    for item in product((-7, 0, 11), repeat=length):
        codes = list(item)
        output, result, group, final_char = operational_decode(codes)
        assert decode_codes(codes) == output
        assert decoded_result([], codes) == result
        assert decoded_tail(codes) == group
        assert final_loop_char(codes, ("old",)) == final_char
        checked += 1

adversarial = [
    [],
    [1],
    [1, 2],
    [1, 2, 3],
    [1, 2, 3, 4],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5, 6],
    [-99, 0, 42, 42, -1, 8, 1000, 1000],
]
for codes in adversarial:
    output, _, _, _ = operational_decode(codes)
    print(f"codes={codes} operational={output} summary={decode_codes(codes)}")

witness = [1, 2, 3]
correct = decode_codes(witness)
counterfactuals = {
    "identity": witness,
    "constant_empty": [],
    "left_rotation": [2, 3, 1],
}
for name, value in counterfactuals.items():
    print(
        f"counterfactual={name} witness={witness} value={value} "
        f"correct={correct} rejected={value != correct}"
    )
    assert value != correct

print(f"exhaustive_cases={checked}")
print("mismatches=0")
