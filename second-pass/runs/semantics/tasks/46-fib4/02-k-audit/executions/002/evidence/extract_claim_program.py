#!/usr/bin/env python3
"""Extract the closure executed by operational-cases as an MPY module.

This is a constructor-level comparison aid: the closure arguments are parsed by
balanced delimiters, wrapped back into FuncDef/Module syntax, and then both this
term and solution.mpy are parsed by K's own `kast`.
"""

from pathlib import Path


SPEC = Path("/tmp/audit-work/46-fib4-review/spec.k")
OUTPUT = Path("/tmp/audit-work/46-fib4-review/claim-executed.mpy")


def matching_paren(text: str, opening: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
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
                return index
    raise ValueError("unbalanced closureVal")


def split_top_level(text: str) -> list[str]:
    parts = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(text):
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
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


text = SPEC.read_text()
marker = '"fib4" |-> closureVal('
marker_index = text.index(marker)
opening = marker_index + len(marker) - 1
closing = matching_paren(text, opening)
args = split_top_level(text[opening + 1 : closing])
if len(args) != 3:
    raise ValueError(f"expected 3 closureVal arguments, found {len(args)}")
params, body, defining_scope = args
if params != '("n", .ParamNames)':
    raise ValueError(f"unexpected parameters: {params}")
if defining_scope != "0":
    raise ValueError(f"unexpected defining scope: {defining_scope}")

# In a K claim, singleton/empty Stmts arguments are printed explicitly as
# `Stmt .Stmts` / `.Stmts`.  The MPY program parser uses the surface list
# notation instead.  Removing only those explicit empty-list units is the
# corresponding semantically inert surface normalization.
surface_body = body.replace(".Stmts", "")
OUTPUT.write_text(
    f'Module(\n  FuncDef("fib4", Params("n"),\n{surface_body}))\n'
)
print(f"marker_offset={marker_index}")
print(f"closure_arg_count={len(args)}")
print(f"params={params}")
print(f"defining_scope={defining_scope}")
print(f"body_chars={len(body)}")
print("normalization=removed explicit .Stmts list units")
print(f"output={OUTPUT}")
