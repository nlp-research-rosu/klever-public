#!/usr/bin/env python3
"""Independent differential audit for HumanEval 119-match-parens.

Oracles:
  * trusted dataset implementation: /reference/canonical.py
  * an independently written balance predicate below
Subject:
  * scratch copy of the candidate's generated solution.py

Scope:
  * all pairs of parenthesis-only strings of length 0..7;
  * documented and targeted branch/boundary cases;
  * 5,000 deterministic random pairs with lengths 0..128.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path

CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/audit-119-match-parens/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.match_parens


def balanced(text: str) -> bool:
    depth = 0
    for char in text:
        depth += 1 if char == "(" else -1
        if depth < 0:
            return False
    return depth == 0


def independent_oracle(pair: list[str]) -> str:
    left, right = pair
    return "Yes" if balanced(left + right) or balanced(right + left) else "No"


def all_strings(max_length: int):
    for length in range(max_length + 1):
        for chars in itertools.product("()", repeat=length):
            yield "".join(chars)


canonical = load_entry(CANONICAL_PATH, "trusted_canonical_119")
generated = load_entry(GENERATED_PATH, "candidate_generated_119")

documented_and_boundaries = [
    ["()(", ")"],               # documented Yes; first order works
    [")", ")"],                 # documented No
    ["", ""],                   # empty boundary
    [")", "("],                 # only second order works
    ["(", ")"],                 # only first order works
    ["()", "()"],               # both orders work
    ["(()", "("],               # positive final depth, neither works
    ["))", "(("],               # second order works at a deep boundary
    ["((", "))"],               # first order works at a deep boundary
    [")(", ""],                 # prefix-negative in the only distinct order
    ["(" * 256, ")" * 256],     # long balanced first order
    [")" * 256, "(" * 256],     # long balanced second order
    ["()" * 128, ""],           # long already-balanced string
    ["(" * 255, ")" * 254],     # long unmatched open
]

mismatches: list[tuple[list[str], str, str, str]] = []
branch_counts = {"both": 0, "first_only": 0, "second_only": 0, "neither": 0}
seen: set[tuple[str, str]] = set()


def check(pair: list[str]) -> None:
    key = (pair[0], pair[1])
    if key in seen:
        return
    seen.add(key)
    expected = independent_oracle(pair)
    canonical_result = canonical(pair)
    generated_result = generated(pair)
    first = balanced(pair[0] + pair[1])
    second = balanced(pair[1] + pair[0])
    bucket = (
        "both"
        if first and second
        else "first_only"
        if first
        else "second_only"
        if second
        else "neither"
    )
    branch_counts[bucket] += 1
    if canonical_result != expected or generated_result != expected:
        mismatches.append((pair, expected, canonical_result, generated_result))


for targeted in documented_and_boundaries:
    check(targeted)

small_strings = list(all_strings(7))
for left in small_strings:
    for right in small_strings:
        check([left, right])

rng = random.Random(119)
for _ in range(5_000):
    left = "".join(rng.choice("()") for _ in range(rng.randrange(129)))
    right = "".join(rng.choice("()") for _ in range(rng.randrange(129)))
    check([left, right])

print(f"canonical={CANONICAL_PATH}")
print(f"generated={GENERATED_PATH}")
print("targeted_cases=", len(documented_and_boundaries))
print("exhaustive_strings=", len(small_strings))
print("checked_pairs=", len(seen))
print("branch_counts=", branch_counts)
print("mismatch_count=", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))

if mismatches:
    raise SystemExit(1)
