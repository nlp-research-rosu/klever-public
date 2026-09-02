#!/usr/bin/env python3
"""Mechanical constructor-level pinning checks for the submitted program."""

from __future__ import annotations

import re
from pathlib import Path


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def balanced_argument(text: str, call_prefix: str, argument_index: int) -> str:
    """Return a top-level call argument from compact constructor text."""
    start = text.index(call_prefix) + len(call_prefix)
    depth = 0
    in_string = False
    escaped = False
    arguments: list[str] = []
    argument_start = start
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
            if depth == 0:
                arguments.append(text[argument_start:index])
                return arguments[argument_index]
            depth -= 1
        elif char == "," and depth == 0:
            arguments.append(text[argument_start:index])
            argument_start = index + 1
    raise ValueError(f"unbalanced constructor beginning {call_prefix!r}")


solution = compact(Path("/candidate/solution.mpy").read_text(encoding="utf-8"))
verification_text = Path("/candidate/verification.k").read_text(encoding="utf-8")

assert solution.startswith('Module(FuncDef("encrypt",Params("s"),')
function_term = balanced_argument(solution, "Module(", 0)
function_name = balanced_argument(function_term, "FuncDef(", 0)
function_params = balanced_argument(function_term, "FuncDef(", 1)
function_body = balanced_argument(function_term, "FuncDef(", 2)

function_macro_match = re.search(
    r"rule\s+encryptFunctionBody\s*=>\s*(.*?)\s*\.Stmts"
    r"\s*syntax\s+Val",
    verification_text,
    flags=re.DOTALL,
)
assert function_macro_match is not None
function_macro_body = compact(function_macro_match.group(1))

loop_macro_match = re.search(
    r"rule\s+encryptLoopBody\s*=>\s*(.*?)\s*\.Stmts"
    r"\s*syntax\s+Stmts\s*::=\s*\"encryptFunctionBody\"",
    verification_text,
    flags=re.DOTALL,
)
assert loop_macro_match is not None
loop_macro_body = compact(loop_macro_match.group(1))
source_loop_body = balanced_argument(function_body, "For(", 2)
expanded_function_macro_body = function_macro_body.replace(
    "encryptLoopBody", loop_macro_body
)

closure_match = re.search(
    r"rule\s+encryptClosure\s*=>\s*(closureVal\(.*?\))\s*endmodule",
    verification_text,
    flags=re.DOTALL,
)
assert closure_match is not None
closure_rhs = compact(closure_match.group(1))
closure_expected = 'closureVal("s",encryptFunctionBody,0)'

print(f"top_level_function_name={function_name}")
print(f"top_level_function_params={function_params}")
print(
    "function_body_constructor_match="
    f"{function_body == expanded_function_macro_body}"
)
print(f"loop_body_constructor_match={source_loop_body == loop_macro_body}")
print(f"closure_binding_match={closure_rhs == closure_expected}")
print(f"function_body_compact={function_body}")
print(f"loop_body_compact={source_loop_body}")
print(f"closure_rhs_compact={closure_rhs}")

if not (
    function_name == '"encrypt"'
    and function_params == 'Params("s")'
    and function_body == expanded_function_macro_body
    and source_loop_body == loop_macro_body
    and closure_rhs == closure_expected
):
    raise SystemExit(1)
