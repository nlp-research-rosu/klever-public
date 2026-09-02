#!/usr/bin/env python3
"""Independent executable sanity checks for the frozen source and scan definition."""

from __future__ import annotations

from itertools import product


def source_from_state(state: int, text: str) -> bool:
    for bracket in text:
        if bracket == "[":
            if state < 2:
                state += 1
        else:
            if state == 2:
                state = 3
            elif state == 3:
                return True
    return False


TRANSITIONS: dict[tuple[int, str], int | bool] = {
    (0, "["): 1,
    (0, "]"): 0,
    (1, "["): 2,
    (1, "]"): 1,
    (2, "["): 2,
    (2, "]"): 3,
    (3, "["): 3,
    (3, "]"): True,
}


def scan(state: int, text: str, transitions=TRANSITIONS, base=False) -> bool:
    for bracket in text:
        result = transitions[(state, bracket)]
        if result is True:
            return True
        state = result
    return base


def has_nested_subsequence(text: str) -> bool:
    pattern = iter("[[]]")
    wanted = next(pattern, None)
    for character in text:
        if character == wanted:
            wanted = next(pattern, None)
            if wanted is None:
                return True
    return False


def all_bracket_strings(max_length: int):
    for length in range(max_length + 1):
        for characters in product("[]", repeat=length):
            yield "".join(characters)


examples = {
    "[[]]": True,
    "[]]]]]]][[[[[]": False,
    "[][]": False,
    "[]": False,
    "[[][]]": True,
    "[[]][[": True,
    "": False,
    "]]]][[[[": False,
    "[[[]]]": True,
    "[[[]": False,
}
for text, expected in examples.items():
    observed = source_from_state(0, text)
    print(f"example {text!r}: source={observed} scan={scan(0, text)} expected={expected}")
    assert observed == scan(0, text) == expected

checked = 0
for text in all_bracket_strings(12):
    for state in range(4):
        assert source_from_state(state, text) == scan(state, text)
        checked += 1
    assert scan(0, text) == has_nested_subsequence(text)
print(f"exhaustive_source_scan_state_cases={checked}")
print("exhaustive_max_length=12")
print("exhaustive_mismatches=0")

mutations: dict[str, tuple[tuple[int, str] | None, int | bool]] = {
    "base_false_to_true": (None, True),
    "scan_0_lbr": ((0, "["), 0),
    "scan_0_rbr": ((0, "]"), 1),
    "scan_1_lbr": ((1, "["), 1),
    "scan_1_rbr": ((1, "]"), 0),
    "scan_2_lbr": ((2, "["), 3),
    "scan_2_rbr": ((2, "]"), 2),
    "scan_3_lbr": ((3, "["), 0),
    "scan_3_rbr_accept": ((3, "]"), 3),
}
for name, (key, replacement) in mutations.items():
    mutated = dict(TRANSITIONS)
    base = False
    if key is None:
        base = bool(replacement)
    else:
        mutated[key] = replacement
    witness = next(
        (
            text
            for text in all_bracket_strings(10)
            if scan(0, text) != scan(0, text, mutated, base)
        ),
        None,
    )
    print(f"counterfactual {name}: witness={witness!r}")
    assert witness is not None

print("counterfactual_mutations_distinguished=9")
