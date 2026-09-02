#!/usr/bin/env python3
"""Mechanically compare the translated function body with the closure adapter."""

from __future__ import annotations

from pathlib import Path


def balanced_term(text: str, marker: str) -> str:
    start = text.index(marker)
    open_at = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_at, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced term beginning with {marker!r}")


def arguments(term: str) -> list[str]:
    open_at = term.index("(")
    inner = term[open_at + 1 : -1]
    result: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(inner):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(inner[start:index])
            start = index + 1
    result.append(inner[start:])
    return result


def normalize(text: str) -> str:
    normalized = "".join(text.split())
    normalized = normalized.replace(",.Exprs)", ",)")
    normalized = normalized.replace(",.Stmts)", ",)")
    return normalized


translated = Path(
    "/tmp/audit-work/candidate/solution.regenerated.mpy"
).read_text()
verification = Path(
    "/tmp/audit-work/candidate/verification.k"
).read_text()

module = balanced_term(translated, "Module")
module_args = arguments(module)
assert len(module_args) == 1
func_def = balanced_term(module_args[0], "FuncDef")
func_args = arguments(func_def)
assert len(func_args) == 3

closure = balanced_term(verification, "closureVal")
closure_args = arguments(closure)
assert len(closure_args) == 3

function_name, params, translated_body = func_args
closure_params, closure_body, closure_scope = closure_args

assert normalize(function_name) == '"check_if_last_char_is_a_letter"'
assert normalize(params) == 'Params("txt")'
assert normalize(closure_params) == '"txt"'
assert normalize(closure_scope) == "0"
assert normalize(translated_body) == normalize(closure_body)

print("function_name=check_if_last_char_is_a_letter")
print("translated_params=Params(\"txt\")")
print("closure_params=\"txt\"")
print("closure_lexical_scope=0")
print("normalization=whitespace plus explicit .Exprs/.Stmts empty-list spelling")
print("constructor_body_identity=true")
