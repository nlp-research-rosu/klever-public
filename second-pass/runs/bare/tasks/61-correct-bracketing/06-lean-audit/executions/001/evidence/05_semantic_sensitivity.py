#!/usr/bin/env python3
"""Finite adversarial support for the independent rule classification.

The universal classification judgment remains the source-level branch/recurrence
analysis in REVIEW.md. This executable evidence checks boundary cases and shows
that counterfactual changes to every bracketSpec equation alter behavior.
"""

from __future__ import annotations

import itertools


def frozen_operational_suffix(depth: int, text: str) -> bool:
    """The inspected solution.py/semantic.k loop behavior."""
    for character in text:
        if character == "(":
            depth += 1
        else:
            if depth == 0:
                return False
            depth -= 1
    return depth == 0


def classified_bracket_spec(depth: int, text: str) -> bool:
    """The four inspected bracketSpec defining equations."""
    if text == "":
        return depth == 0
    if text[0] == "(":
        return classified_bracket_spec(depth + 1, text[1:])
    if depth == 0:
        return False
    return classified_bracket_spec(depth - 1, text[1:])


checked = 0
for depth in range(9):
    for length in range(9):
        for characters in itertools.product("()x", repeat=length):
            text = "".join(characters)
            observed = classified_bracket_spec(depth, text)
            expected = frozen_operational_suffix(depth, text)
            assert observed == expected, (depth, text, observed, expected)
            checked += 1
print(f"operational_summary_comparisons={checked}")
print("operational_summary_mismatches=0")

boundaries = [
    (0, "", True),
    (1, "", False),
    (0, "(", False),
    (0, ")", False),
    (1, ")", True),
    (0, "()", True),
    (0, ")(()", False),
    (0, "(()())", True),
    (0, "x", False),
]
for depth, text, expected in boundaries:
    actual = classified_bracket_spec(depth, text)
    print(
        f"boundary depth={depth} text={text!r} "
        f"expected={expected} actual={actual}"
    )
    assert actual == expected


def mutated_base(depth: int, text: str) -> bool:
    if text == "":
        return True
    return classified_bracket_spec(depth, text)


def mutated_open(depth: int, text: str) -> bool:
    if text and text[0] == "(":
        return classified_bracket_spec(depth, text[1:])
    return classified_bracket_spec(depth, text)


def mutated_zero_close(depth: int, text: str) -> bool:
    if text and text[0] != "(" and depth == 0:
        return True
    return classified_bracket_spec(depth, text)


def mutated_positive_close(depth: int, text: str) -> bool:
    if text and text[0] != "(" and depth > 0:
        return classified_bracket_spec(depth + 1, text[1:])
    return classified_bracket_spec(depth, text)


mutations = [
    ("base_always_true", mutated_base, 1, ""),
    ("open_does_not_increment", mutated_open, 0, "()"),
    ("zero_close_accepts", mutated_zero_close, 0, ")"),
    ("positive_close_increments", mutated_positive_close, 1, ")"),
]
for name, mutation, depth, text in mutations:
    mutated = mutation(depth, text)
    operational = frozen_operational_suffix(depth, text)
    print(
        f"counterfactual={name} witness_depth={depth} witness_text={text!r} "
        f"mutated={mutated} operational={operational} "
        f"distinguished={mutated != operational}"
    )
    assert mutated != operational

print("all_four_summary_equations_operationally_sensitive=PASS")
print("OVERALL=PASS")
