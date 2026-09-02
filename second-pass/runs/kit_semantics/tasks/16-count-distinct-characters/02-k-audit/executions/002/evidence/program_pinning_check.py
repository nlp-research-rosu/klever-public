#!/usr/bin/env python3
"""Mechanical source-to-claim constructor comparison for the entry closure."""

from __future__ import annotations

import re
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/candidate-src/regenerated-solution.mpy")
SPEC = Path("/tmp/audit-work/candidate-src/spec.k")


def balanced_constructor(text: str, start: int, name: str) -> str:
    prefix = f"{name}("
    if not text.startswith(prefix, start):
        raise AssertionError(f"{prefix!r} not found at offset {start}")
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
    raise AssertionError(f"unterminated {name} constructor")


def first_return(text: str) -> str:
    start = text.index("Return(")
    return balanced_constructor(text, start, "Return")


def normalize_constructor(text: str) -> str:
    normalized = re.sub(r"\s+", "", text)
    normalized = normalized.replace(",.Exprs)", ",)")
    return normalized


solution_text = SOLUTION.read_text(encoding="utf-8")
spec_text = SPEC.read_text(encoding="utf-8")

solution_body = first_return(solution_text)
spec_body = first_return(spec_text)
solution_normalized = normalize_constructor(solution_body)
spec_normalized = normalize_constructor(spec_body)

assert solution_normalized == spec_normalized
assert 'FuncDef("count_distinct_characters", Params("string"),' in re.sub(
    r"\s+", " ", solution_text
)
assert re.search(
    r'"count_distinct_characters"\s*\|->\s*closureVal\s*\(\s*'
    r'\("string",\s*\.ParamNames\)',
    spec_text,
)
assert 'Call(Name("count_distinct_characters"), str(CS:IntSeq))' in re.sub(
    r"\s+", " ", spec_text
)
assert re.search(r"closureVal\s*\(.*?,\s*0\s*\)", spec_text, re.DOTALL)

print("CONSTRUCTOR_BODY_MATCH: true")
print(f"SOLUTION_BODY_NORMALIZED: {solution_normalized}")
print(f"SPEC_BODY_NORMALIZED: {spec_normalized}")
print("FUNCTION_NAME_MATCH: true")
print("PARAMETER_LIST_MATCH: true")
print("CLOSURE_ENVIRONMENT: 0")
print("ENTRY_CALL_ARGUMENT_DOMAIN: str(CS:IntSeq)")
