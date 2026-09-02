#!/usr/bin/env python3
"""Independent differential test for HumanEval/1.

The intended alphabet is parentheses plus spaces.  Exhaustive testing covers
every string over that alphabet through length 9, including invalid strings as
extra characterization.  A second deterministic suite constructs larger valid
sequences of balanced groups and inserts spaces at arbitrary positions.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.separate_paren_groups


CANONICAL = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
)
GENERATED = load_entry(
    Path("/tmp/audit-work/rebuild/solution.py"), "candidate_solution"
)


def is_balanced(text: str) -> bool:
    depth = 0
    for char in text:
        if char == " ":
            continue
        depth += 1 if char == "(" else -1
        if depth < 0:
            return False
    return depth == 0


def one_dyck_group(pairs: int, rng: random.Random) -> str:
    opens = 0
    closes = 0
    chars: list[str] = []
    while closes < pairs:
        choices: list[str] = []
        if opens < pairs:
            choices.append("(")
        if closes < opens:
            choices.append(")")
        char = rng.choice(choices)
        chars.append(char)
        if char == "(":
            opens += 1
        else:
            closes += 1
    return "".join(chars)


def spaced(text: str, rng: random.Random) -> str:
    pieces = [" " * rng.randrange(4)]
    for char in text:
        pieces.append(char)
        pieces.append(" " * rng.randrange(4))
    return "".join(pieces)


def check(text: str, expected=None) -> None:
    canonical = CANONICAL(text)
    generated = GENERATED(text)
    if canonical != generated:
        raise AssertionError(
            f"differential mismatch for {text!r}: "
            f"canonical={canonical!r}, generated={generated!r}"
        )
    if expected is not None and generated != expected:
        raise AssertionError(
            f"wrong expected result for {text!r}: "
            f"expected={expected!r}, actual={generated!r}"
        )


documented = {
    "( ) (( )) (( )( ))": ["()", "(())", "(()())"],
}
boundaries = {
    "": [],
    " ": [],
    "()": ["()"],
    "(())": ["(())"],
    "()()": ["()", "()"],
    "(((())))": ["(((())))"],
    " ( ( ) )  ( ) ": ["(())", "()"],
    "(()())(())()": ["(()())", "(())", "()"],
}

for text, expected in documented.items():
    check(text, expected)
for text, expected in boundaries.items():
    check(text, expected)

alphabet = "() "
exhaustive_count = 0
balanced_count = 0
for length in range(10):
    for chars in itertools.product(alphabet, repeat=length):
        text = "".join(chars)
        check(text)
        exhaustive_count += 1
        balanced_count += int(is_balanced(text))

rng = random.Random(20260726)
generated_inputs: list[str] = []
for _ in range(1000):
    groups = [one_dyck_group(rng.randrange(1, 13), rng) for _ in range(rng.randrange(1, 8))]
    text = spaced("".join(groups), rng)
    check(text)
    generated_inputs.append(text)

# This witnesses why the proof/test domain must remain the documented alphabet.
outside_domain = "(a)"
outside_canonical = CANONICAL(outside_domain)
outside_generated = GENERATED(outside_domain)
assert outside_canonical != outside_generated

print("documented_cases=1 mismatches=0")
print("boundary_cases=8 mismatches=0")
print(
    f"exhaustive_alphabet_strings={exhaustive_count} "
    f"balanced_subset={balanced_count} max_length=9 mismatches=0"
)
print("generated_valid_inputs=1000 seed=20260726 mismatches=0")
print(f"representative_generated_input={generated_inputs[0]!r}")
print(
    "outside_domain_witness="
    f"{outside_domain!r} canonical={outside_canonical!r} generated={outside_generated!r}"
)
