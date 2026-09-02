#!/usr/bin/env python3
"""Independent differential test for HumanEval/1.

The trusted canonical function and submitted function are loaded from distinct
absolute paths. Tests cover named branch boundaries, all balanced parenthesis
words through five pairs with every optional single-space gap placement, all
strings over the generated semantics' LP/RP/SP alphabet through length nine,
and deterministic larger balanced samples.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.separate_paren_groups


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
submitted = load_entry(
    "submitted_solution", Path("/tmp/audit-work/candidate/solution.py")
)


def compare(source: str, expected=None) -> None:
    global comparisons
    oracle_value = canonical(source)
    submitted_value = submitted(source)
    comparisons += 1
    if expected is not None:
        assert oracle_value == expected, (source, oracle_value, expected)
    assert submitted_value == oracle_value, (
        source,
        submitted_value,
        oracle_value,
    )


def dyck_words(pairs: int):
    def visit(prefix: str, opens: int, closes: int):
        if opens == pairs and closes == pairs:
            yield prefix
            return
        if opens < pairs:
            yield from visit(prefix + "(", opens + 1, closes)
        if closes < opens:
            yield from visit(prefix + ")", opens, closes + 1)

    yield from visit("", 0, 0)


def with_optional_gap_spaces(word: str):
    for mask in range(1 << (len(word) + 1)):
        pieces = []
        for index, char in enumerate(word):
            if mask & (1 << index):
                pieces.append(" ")
            pieces.append(char)
        if mask & (1 << len(word)):
            pieces.append(" ")
        yield "".join(pieces)


def random_balanced(rng: random.Random, pairs: int) -> str:
    opens = 0
    closes = 0
    chars = []
    while closes < pairs:
        can_open = opens < pairs
        can_close = closes < opens
        choose_open = can_open and (not can_close or rng.randrange(2) == 0)
        if choose_open:
            chars.append("(")
            opens += 1
        else:
            chars.append(")")
            closes += 1
        if rng.randrange(5) == 0:
            chars.append(" " * rng.randrange(1, 4))
    return (" " * rng.randrange(3)) + "".join(chars) + (" " * rng.randrange(3))


comparisons = 0
named_cases = [
    ("documented example", "( ) (( )) (( )( ))", ["()", "(())", "(()())"]),
    ("empty", "", []),
    ("spaces only", "     ", []),
    ("single group", "()", ["()"]),
    ("space outer-if false", "( )", ["()"]),
    ("nested close stays nonzero", "((()))", ["((()))"]),
    ("adjacent groups", "()(())(()())", ["()", "(())", "(()())"]),
    ("deep nesting", "((((()))))", ["((((()))))"]),
    ("spaces at boundaries", "  ( ( ) )  ( ) ", ["(())", "()"]),
]
for label, source, expected in named_cases:
    compare(source, expected)
    print(f"NAMED PASS: {label}: {source!r} -> {expected!r}")

balanced_inputs = 0
for pair_count in range(0, 6):
    for word in dyck_words(pair_count):
        for source in with_optional_gap_spaces(word):
            compare(source)
            balanced_inputs += 1

alphabet_inputs = 0
for length in range(0, 10):
    for chars in itertools.product("() ", repeat=length):
        compare("".join(chars))
        alphabet_inputs += 1

rng = random.Random(0x5EED)
random_inputs = 250
for _ in range(random_inputs):
    compare(random_balanced(rng, rng.randrange(1, 41)))

print(f"EXHAUSTIVE_BALANCED_WITH_GAP_SPACES={balanced_inputs}")
print(f"EXHAUSTIVE_LP_RP_SP_LENGTH_LE_9={alphabet_inputs}")
print(f"DETERMINISTIC_LARGE_BALANCED={random_inputs}")
print(f"TOTAL_COMPARISONS={comparisons}")
print("MISMATCHES=0")
