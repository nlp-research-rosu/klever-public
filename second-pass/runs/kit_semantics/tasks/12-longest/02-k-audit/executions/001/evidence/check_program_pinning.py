#!/usr/bin/env python3
"""Mechanically compare translated Module constructors with both entry claims."""

from __future__ import annotations

import hashlib
from pathlib import Path


def extract_balanced(text: str, start: int) -> str:
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unterminated constructor term")


def normalize(term: str) -> str:
    """Remove layout and the Stmts identity explicitly inserted in the spec."""
    output: list[str] = []
    quoted = False
    escaped = False
    index = 0
    while index < len(term):
        character = term[index]
        if quoted:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            index += 1
            continue
        if character == '"':
            quoted = True
            output.append(character)
            index += 1
            continue
        if term.startswith(".Stmts", index):
            index += len(".Stmts")
            continue
        if character.isspace():
            index += 1
            continue
        output.append(character)
        index += 1
    return "".join(output)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


solution_text = Path("/candidate/solution.mpy").read_text(encoding="utf-8").strip()
spec_text = Path("/candidate/spec.k").read_text(encoding="utf-8")
solution_term = extract_balanced(solution_text, solution_text.index("Module("))
solution_normal = normalize(solution_term)

starts: list[int] = []
position = 0
while True:
    load_position = spec_text.find("#loadAll(", position)
    if load_position < 0:
        break
    module_position = spec_text.find("Module(", load_position)
    assert module_position >= 0
    starts.append(module_position)
    position = module_position + 1

assert len(starts) == 2, f"expected two entry Module terms, found {len(starts)}"
print(f"solution_normalized_sha256={digest(solution_normal)}")
for index, start in enumerate(starts, 1):
    claim_term = extract_balanced(spec_text, start)
    claim_normal = normalize(claim_term)
    print(f"entry_{index}_normalized_sha256={digest(claim_normal)}")
    assert claim_normal == solution_normal, f"entry {index} executes a different Module"

assert spec_text.count('~> Call(Name("longest"),') == 2
print("PASS: both entry claims execute the normalized submitted Module constructor")
print("PASS: both entry continuations call the submitted binding name longest")
