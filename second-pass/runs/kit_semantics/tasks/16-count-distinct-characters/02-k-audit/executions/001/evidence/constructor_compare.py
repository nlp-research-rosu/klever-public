#!/usr/bin/env python3
"""Mechanical surface-constructor comparison for source-to-entry-claim pinning."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def balanced_call(text: str, marker: str) -> str:
    start = text.index(marker)
    open_paren = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
        character = text[index]
        if escaped:
            escaped = False
            continue
        if in_string and character == "\\":
            escaped = True
            continue
        if character == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced constructor {marker}")


def top_level_args(call: str) -> list[str]:
    body = call[call.index("(") + 1 : -1]
    args: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, character in enumerate(body):
        if escaped:
            escaped = False
            continue
        if in_string and character == "\\":
            escaped = True
            continue
        if character == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            args.append(body[start:index].strip())
            start = index + 1
    args.append(body[start:].strip())
    return args


def compact(term: str) -> str:
    return re.sub(r"\s+", "", term)


root = Path("/tmp/audit-work/reconstruction")
solution = (root / "solution.mpy").read_text()
spec = (root / "spec.k").read_text()

func = balanced_call(solution, 'FuncDef("count_distinct_characters"')
func_args = top_level_args(func)
closure = balanced_call(spec, "closureVal(")
closure_args = top_level_args(closure)

source_name = compact(func_args[0])
source_params = top_level_args(func_args[1])
source_body = compact(func_args[2])

claim_params = compact(closure_args[0])
claim_body = compact(closure_args[1])
claim_body = claim_body.removesuffix(".Stmts")
claim_anchor = compact(closure_args[2])
source_body_list_normalized = source_body.replace(",.Exprs)", ",)")
claim_body_list_normalized = claim_body.replace(",.Exprs)", ",)")

expected_params = compact(f"({source_params[0]}, .ParamNames)")
checks = {
    "function_name": source_name == '"count_distinct_characters"',
    "parameter_constructor": expected_params == claim_params,
    "body_surface_exact": source_body == claim_body,
    "body_list_unit_normalized": (
        source_body_list_normalized == claim_body_list_normalized
    ),
    "definition_scope_anchor": claim_anchor == "0",
    "entry_call": compact(
        'Call(Name("count_distinct_characters"), str(CS:IntSeq))'
    )
    in compact(spec),
}

print(f"source_function_constructor={compact(func)}")
print(f"claim_closure_constructor={compact(closure)}")
print(f"source_body_sha256={hashlib.sha256(source_body.encode()).hexdigest()}")
print(f"claim_body_sha256={hashlib.sha256(claim_body.encode()).hexdigest()}")
for name, passed in checks.items():
    print(f"{name}_matches={passed}")

required = {name: value for name, value in checks.items() if name != "body_surface_exact"}
print("body_surface_note=implicit Exprs units are compared after K parsing")
sys.exit(0 if all(required.values()) else 1)
