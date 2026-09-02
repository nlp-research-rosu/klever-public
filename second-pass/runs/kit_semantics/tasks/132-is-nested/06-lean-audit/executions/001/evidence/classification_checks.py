#!/usr/bin/env python3
"""Finite sensitivity checks supplementing the source-level classification audit."""

from itertools import product


def source_model(text: str) -> bool:
    state = 0
    bracket = ""
    for bracket in text:
        if state < 2:
            if bracket == "[":
                state += 1
        elif state < 4:
            if bracket == "]":
                state += 1
    return state == 4


def nested_step(code: int, state: int) -> int:
    if state < 2 and code == 91:
        return state + 1
    if state < 2 and code != 91:
        return state
    if state >= 2 and state < 4 and code == 93:
        return state + 1
    if state >= 2 and state < 4 and code != 93:
        return state
    if state >= 4:
        return state
    raise AssertionError("the guarded equations were not total")


def nested_scan(codes: tuple[int, ...], state: int) -> int:
    if not codes:
        return state
    return nested_scan(codes[1:], nested_step(codes[0], state))


def nested_result(text: str) -> bool:
    return nested_scan(tuple(map(ord, text)), 0) == 4


samples = ["", "[]", "[][]", "[[]]", "[[][]]", "[[]][[", "[]]]]]]][[[[[]"]
for sample in samples:
    print(f"sample={sample!r} source={source_model(sample)} summary={nested_result(sample)}")

mismatches = []
tested = 0
for length in range(11):
    for chars in product("[]", repeat=length):
        text = "".join(chars)
        tested += 1
        if source_model(text) != nested_result(text):
            mismatches.append(text)
print(f"exhaustive_bracket_strings_length_0_through_10={tested}")
print(f"mismatch_count={len(mismatches)}")


def mutated_step_early(code: int, state: int) -> int:
    if state < 2:
        return state + 1 if code == 93 else state
    return state + 1 if state < 4 and code == 93 else state


def mutated_step_late(code: int, state: int) -> int:
    if state < 2:
        return state + 1 if code == 91 else state
    return state + 1 if state < 4 and code == 91 else state


def scan_with(text: str, step) -> int:
    state = 0
    for character in text:
        state = step(ord(character), state)
    return state


print(
    "counterfactual early-code 91->93 on '[[]]':",
    source_model("[[]]"),
    scan_with("[[]]", mutated_step_early) == 4,
)
print(
    "counterfactual late-code 93->91 on '[[]]':",
    source_model("[[]]"),
    scan_with("[[]]", mutated_step_late) == 4,
)
print(
    "counterfactual nestedResult ==3 on '[][]':",
    source_model("[][]"),
    nested_scan(tuple(map(ord, "[][]")), 0) == 3,
)

assert not mismatches
