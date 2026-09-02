#!/usr/bin/env python3
"""Check finite representatives of the symbolic path-condition partitions."""

from __future__ import annotations

import itertools
import re
from pathlib import Path


def input_length(term: str) -> int:
    return term.count("cons(")


def satisfies(condition: str, bindings: dict[str, int]) -> bool:
    clauses = re.split(r"\s+andBool\s+", condition)
    for clause in clauses:
        match = re.fullmatch(r"\s*([A-D])\s*(<=Int|>Int)\s*([A-D])\s*", clause)
        assert match is not None, clause
        left, operator, right = match.groups()
        if operator == "<=Int" and not bindings[left] <= bindings[right]:
            return False
        if operator == ">Int" and not bindings[left] > bindings[right]:
            return False
    return True


spec = Path("/candidate/spec.k").read_text()
chunks = re.split(r"(?m)^\s*claim\s*$", spec)[1:]
conditions: dict[int, list[str]] = {2: [], 3: [], 4: []}
for chunk in chunks:
    input_match = re.search(r"<input>\s*(.*?)\s*</input>", chunk, re.S)
    requires_match = re.search(r"(?m)^\s*requires\s+(.*?)\s*$", chunk)
    assert input_match is not None
    length = input_length(input_match.group(1))
    if length in conditions and requires_match is not None:
        conditions[length].append(requires_match.group(1))

assert {length: len(values) for length, values in conditions.items()} == {
    2: 2,
    3: 6,
    4: 24,
}

for length, preconditions in conditions.items():
    variables = "ABCD"[:length]
    checked = 0
    for values in itertools.product(range(-3, 4), repeat=length):
        bindings = dict(zip(variables, values))
        matches = [
            index
            for index, condition in enumerate(preconditions, 1)
            if satisfies(condition, bindings)
        ]
        assert len(matches) == 1, (length, bindings, matches)
        checked += 1
    print(
        f"length={length} partitions={len(preconditions)} "
        f"representative_assignments={checked} every_assignment_exactly_one=true"
    )

print("PARTITION CHECK PASS")
