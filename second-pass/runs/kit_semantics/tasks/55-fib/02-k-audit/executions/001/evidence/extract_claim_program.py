#!/usr/bin/env python3
"""Reconstruct an MPY module from the exact closure term in SPEC.fib-call."""

from __future__ import annotations

from pathlib import Path


SPEC = Path("/tmp/audit-work/fib-audit/spec.k")


def balanced_call(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
    raise ValueError("unterminated closureVal call")


def split_args(call: str) -> list[str]:
    inside = call[call.index("(") + 1 : -1]
    args = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(inside):
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
            args.append(inside[start:index].strip())
            start = index + 1
    args.append(inside[start:].strip())
    return args


text = SPEC.read_text(encoding="utf-8")
needle = '"fib" |-> closureVal('
start = text.index("closureVal(", text.index(needle))
call = balanced_call(text, start)
arguments = split_args(call)
assert len(arguments) == 4, arguments
parameter, remaining_parameters, body, parent_scope = arguments
assert parameter == '"n"'
assert remaining_parameters == ".ParamNames"
assert parent_scope == "0"
assert body.rstrip().endswith(".Stmts")
body = body.rstrip()[: -len(".Stmts")].rstrip()

print("Module(")
print(f"  FuncDef(\"fib\", Params({parameter}),")
for line in body.splitlines():
    print(f"    {line.strip()}")
print("  )")
print(")")
