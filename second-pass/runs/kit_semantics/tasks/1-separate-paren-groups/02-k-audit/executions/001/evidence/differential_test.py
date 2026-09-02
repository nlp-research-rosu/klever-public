#!/usr/bin/env python3
"""Independent differential test for HumanEval/1 on its intended domain."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.separate_paren_groups


canonical = load_entry("/reference/canonical.py", "trusted_canonical")
generated = load_entry("/candidate/solution.py", "generated_solution")


def valid_intended_input(text: str) -> bool:
    depth = 0
    for char in text:
        if char == " ":
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                return False
            depth -= 1
        else:
            return False
    return depth == 0


documented_and_boundaries = [
    "( ) (( )) (( )( ))",
    "",
    " ",
    "     ",
    "()",
    "( )",
    "()()",
    "() ()",
    "(())",
    "((()))",
    "(()())",
    "(())()(()())",
    " ( ( ) ) ( ) ",
]

cases = set(documented_and_boundaries)
for length in range(10):
    for chars in itertools.product(" ()", repeat=length):
        text = "".join(chars)
        if valid_intended_input(text):
            cases.add(text)

rng = random.Random(0x5EED)
for _ in range(500):
    groups = []
    for _ in range(rng.randrange(0, 8)):
        pairs = rng.randrange(1, 16)
        opens = pairs
        closes = pairs
        depth = 0
        pieces = []
        while opens or closes:
            can_open = opens > 0
            can_close = closes > 0 and depth > 0
            if can_open and (not can_close or rng.randrange(2) == 0):
                pieces.append("(")
                opens -= 1
                depth += 1
            else:
                pieces.append(")")
                closes -= 1
                depth -= 1
            if rng.randrange(5) == 0:
                pieces.append(" " * rng.randrange(1, 4))
        groups.append("".join(pieces))
    cases.add((" " * rng.randrange(0, 3)).join(groups))

mismatches = []
for text in sorted(cases):
    expected = canonical(text)
    actual = generated(text)
    if expected != actual:
        mismatches.append((text, expected, actual))

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print(f"total_valid_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(repr(mismatch))

# These cases are intentionally outside the contract and are diagnostics only.
outside_domain = [")(", "(()", "abc", "(a)", "()x()"]
print("outside_domain_diagnostics:")
for text in outside_domain:
    print(
        f"  {text!r}: canonical={canonical(text)!r}, generated={generated(text)!r}"
    )

if mismatches:
    raise SystemExit(1)
