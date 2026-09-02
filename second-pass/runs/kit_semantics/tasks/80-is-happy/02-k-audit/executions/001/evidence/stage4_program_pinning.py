#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and the entry claim."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TOKEN = re.compile(
    r'''
    "(?:\\.|[^"\\])*"
    | \.[A-Za-z][A-Za-z0-9]*
    | \#[A-Za-z][A-Za-z0-9]*
    | [A-Za-z_?][A-Za-z0-9_?'-]*
    | -?[0-9]+
    | [()[\],:]
    ''',
    re.VERBOSE,
)


def tokens(path: Path) -> list[str]:
    text = re.sub(r"//[^\n]*", "", path.read_text(encoding="utf-8"))
    return TOKEN.findall(text)


def constructor_args(stream: list[str], name_index: int) -> list[list[str]]:
    assert stream[name_index + 1] == "(", (stream[name_index], stream[name_index + 1])
    args: list[list[str]] = []
    current: list[str] = []
    depth = 0
    cursor = name_index + 2
    while cursor < len(stream):
        token = stream[cursor]
        if token == "(":
            depth += 1
            current.append(token)
        elif token == ")":
            if depth == 0:
                args.append(current)
                return args
            depth -= 1
            current.append(token)
        elif token == "," and depth == 0:
            args.append(current)
            current = []
        else:
            current.append(token)
        cursor += 1
    raise AssertionError(f"unterminated constructor at token {name_index}")


solution_path = Path(sys.argv[1])
spec_path = Path(sys.argv[2])
functions_path = Path(sys.argv[3])

solution_tokens = tokens(solution_path)
spec_tokens = tokens(spec_path)

module_index = solution_tokens.index("Module")
module_args = constructor_args(solution_tokens, module_index)
assert len(module_args) == 1
assert module_args[0][:2] == ["FuncDef", "("]
function_args = constructor_args(module_args[0], 0)
assert len(function_args) == 3
assert function_args[0] == ['"is_happy"']
assert function_args[1] == ["Params", "(", '"s"', ")"]
solution_body = function_args[2]

closure_index = spec_tokens.index("closureVal")
closure_args = constructor_args(spec_tokens, closure_index)
assert len(closure_args) == 3
assert '"is_happy"' in spec_tokens[max(0, closure_index - 12) : closure_index]
assert closure_args[0] == ["(", '"s"', ",", ".ParamNames", ")"]
assert closure_args[2] == ["0"]
claim_body = [token for token in closure_args[1] if token != ".Stmts"]

# The translator renders an empty statement sequence as an empty argument in
# `If(..., then, )`; the K parser spells that same term `.Stmts`.
assert solution_body == claim_body

functions_text = functions_path.read_text(encoding="utf-8")
assert re.search(
    r"FuncDef\(F:String, Params\(PNS:ParamNames\), BODY:Stmts\) => \.K",
    functions_text,
)
assert "F <- closureVal(PNS, BODY, L)" in functions_text

print(f"solution_module_top_level_terms={len(module_args)}")
print("solution_binding=is_happy")
print("solution_parameters=Params(\"s\")")
print("claim_closure_parameters=(\"s\", .ParamNames)")
print(f"solution_body_tokens={len(solution_body)}")
print(f"claim_body_tokens_after_empty_stmts_normalization={len(claim_body)}")
print("constructor_level_body_identity=true")
print("fixed_FuncDef_rule_stores_same_parameter_names_body_and_defining_env=true")
print("claim_closure_defining_env=0")
