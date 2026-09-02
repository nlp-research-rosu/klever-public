#!/usr/bin/env python3
"""Mechanically compare the regenerated Module term with SFTest's module body."""

from __future__ import annotations

import re
from pathlib import Path


def balanced_call(text: str, constructor: str, start: int = 0) -> str:
    begin = text.index(constructor + "(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(begin, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[begin : index + 1]
    raise ValueError(f"unterminated {constructor} term")


def compact(term: str) -> str:
    return re.sub(r"\s+", "", term)


def constructor_tokens(term: str) -> list[str]:
    """Tokenize constructor syntax and normalize K's explicit empty Stmts."""
    tokens = re.findall(
        r'"(?:\\.|[^"\\])*"|[A-Za-z.#][A-Za-z0-9_.#-]*|-?[0-9]+|[(),]',
        term,
    )
    # Stmts is List{Stmt, ""}; the translator prints its empty element as an
    # omitted list item while verification.k spells the same unit as .Stmts.
    return [token for token in tokens if token != ".Stmts"]


regenerated = Path(
    "/tmp/audit-work/candidate-src/solution.regenerated.mpy"
).read_text(encoding="utf-8")
verification = Path(
    "/tmp/audit-work/candidate-src/verification.k"
).read_text(encoding="utf-8")

module_from_program = balanced_call(regenerated, "Module")
sf_rule_start = verification.index("SFTest(ARG) => Run(")
module_from_rule = balanced_call(verification, "Module", sf_rule_start)
call_from_rule = balanced_call(verification, "Call", sf_rule_start)

assert compact(regenerated) == compact(module_from_program)
assert constructor_tokens(module_from_program) == constructor_tokens(module_from_rule)
assert compact(call_from_rule) == 'Call(Name("specialFilter"),ARG)'

print("REGENERATED_IS_ONE_MODULE_TERM True")
print("SFTEST_MODULE_EQUALS_REGENERATED_MODULE True")
print("NORMALIZATION explicit .Stmts equals omitted empty Stmts list")
print("SFTEST_CALL_EQUALS_SPECIALFILTER_ARG True")
print(f"MODULE_COMPACT_LENGTH {len(compact(module_from_program))}")
