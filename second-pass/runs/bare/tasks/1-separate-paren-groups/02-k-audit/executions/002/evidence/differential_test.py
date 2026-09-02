#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential tests on the stated domain."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import random


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.separate_paren_groups


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "candidate_solution"
)

documented = [
    "",
    "()",
    "( )",
    "(())",
    "()()",
    "(()())",
    "( ) (( )) (( )( ))",
    "(((())))",
    "()(())(()())",
    "   ()   ",
]


def is_contract_input(text: str) -> bool:
    depth = 0
    for char in text:
        if char == " ":
            continue
        depth += 1 if char == "(" else -1
        if depth < 0:
            return False
    return depth == 0


cases = list(documented)

# Exhaustively cover every balanced parentheses/space string through length 9.
for size in range(10):
    for chars in product("() ", repeat=size):
        text = "".join(chars)
        if is_contract_input(text):
            cases.append(text)

# Add deterministic larger valid strings, including deep and many-group cases.
rng = random.Random(20260726)
for _ in range(1000):
    pairs = rng.randint(1, 60)
    opens = 0
    closes = 0
    core = []
    while closes < pairs:
        may_open = opens < pairs
        may_close = closes < opens
        if may_open and (not may_close or rng.random() < 0.56):
            core.append("(")
            opens += 1
        else:
            core.append(")")
            closes += 1
    spaced = []
    for char in core:
        spaced.extend(" " * rng.randint(0, 3))
        spaced.append(char)
    spaced.extend(" " * rng.randint(0, 3))
    cases.append("".join(spaced))

unique_cases = list(dict.fromkeys(cases))
mismatches = []
for text in unique_cases:
    expected = canonical(text)
    observed = candidate(text)
    if expected != observed:
        mismatches.append((text, expected, observed))

print(f"documented_and_boundary_cases={len(documented)}")
print("exhaustive_alphabet=() plus space; lengths=0..9; balanced-prefix/final-depth-zero")
print("random_seed=20260726")
print("random_larger_cases=1000; pairs=1..60")
print(f"unique_contract_cases={len(unique_cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")
assert not mismatches
print("DIFFERENTIAL_OK")
