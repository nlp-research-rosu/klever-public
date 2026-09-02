#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy and multiplyClosure."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("/tmp/audit-work/97-multiply")


def normalize(text: str) -> str:
    out: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    return "".join(out)


def extract_call(text: str, marker: str) -> str:
    start = text.index(marker)
    open_paren = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
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
                return text[start:index + 1]
    raise ValueError(f"unbalanced call after {marker!r}")


def split_top_level_args(call: str) -> list[str]:
    body = call[call.index("(") + 1:-1]
    args: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(body):
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
            args.append(body[start:index])
            start = index + 1
    args.append(body[start:])
    return [normalize(arg) for arg in args]


solution_text = (ROOT / "solution.mpy").read_text(encoding="utf-8")
verification_text = (ROOT / "verification.k").read_text(encoding="utf-8")

function_call = extract_call(solution_text, "FuncDef(")
function_args = split_top_level_args(function_call)
if len(function_args) != 3:
    raise AssertionError(f"expected 3 FuncDef arguments, got {len(function_args)}")
name, params_call, body = function_args
if name != '"multiply"':
    raise AssertionError(f"wrong function binding: {name}")

params = split_top_level_args(params_call)
if params != ['"a"', '"b"']:
    raise AssertionError(f"wrong parameters: {params}")

actual_closure = normalize(extract_call(verification_text, "closureVal("))
expected_closure = normalize(
    f"closureVal(({','.join(params)}),({body}),0)"
)
match = actual_closure == expected_closure

print("function_binding=multiply")
print("parameters=a,b")
print("solution_body_sha256=" + hashlib.sha256(body.encode()).hexdigest())
print("expected_closure_sha256=" + hashlib.sha256(expected_closure.encode()).hexdigest())
print("actual_closure_sha256=" + hashlib.sha256(actual_closure.encode()).hexdigest())
print(f"constructor_level_match={match}")

raise SystemExit(0 if match else 1)
