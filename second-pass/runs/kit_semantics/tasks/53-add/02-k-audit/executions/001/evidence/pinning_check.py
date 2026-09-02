#!/usr/bin/env python3
"""Mechanical constructor-level pinning checks for the entry claim."""

from __future__ import annotations

import ast
import re
from pathlib import Path


TOKEN = re.compile(
    r'''
    "(?:\\.|[^"\\])*" |
    [A-Za-z_#$][A-Za-z0-9_#$-]* |
    -?[0-9]+ |
    => | ~> | \|-> |
    [(),.:+\-]
    ''',
    re.VERBOSE,
)


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def balanced_call_argument(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    depth = 1
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
                return text[start:index]
    raise ValueError(f"unbalanced call after {marker!r}")


solution_path = Path("/tmp/audit-work/reconstruction/solution.py")
canonical_path = Path("/reference/canonical.py")
mpy_path = Path("/tmp/audit-work/reconstruction/solution.regenerated.mpy")
spec_path = Path("/tmp/audit-work/reconstruction/spec.k")

solution_ast = ast.parse(solution_path.read_text())
canonical_ast = ast.parse(canonical_path.read_text())

solution_function = next(
    node for node in solution_ast.body if isinstance(node, ast.FunctionDef)
)
canonical_function = next(
    node for node in canonical_ast.body if isinstance(node, ast.FunctionDef)
)

assert solution_function.name == canonical_function.name == "add"
assert [arg.arg for arg in solution_function.args.args] == ["x", "y"]
assert [arg.arg for arg in canonical_function.args.args] == ["x", "y"]
assert len(solution_function.body) == 1
assert isinstance(solution_function.body[0], ast.Return)
assert ast.dump(solution_function.body[0], include_attributes=False) == ast.dump(
    canonical_function.body[-1], include_attributes=False
)

mpy = mpy_path.read_text()
spec = spec_path.read_text()
claim_program = balanced_call_argument(spec, "#loadAll(")
mpy_tokens = tokens(mpy)
claim_tokens = tokens(claim_program)
assert mpy_tokens == claim_tokens

expected = tokens(
    'Module(FuncDef("add", Params("x", "y"), '
    'Return(BinOp("+", Name("x"), Name("y")))))'
)
assert mpy_tokens == expected

closure_body = balanced_call_argument(spec, "closureVal(")
closure_tokens = tokens(closure_body)
expected_closure = tokens(
    '"x", "y", .ParamNames, '
    'Return(BinOp("+", Name("x"), Name("y"))) .Stmts, 0'
)
assert closure_tokens == expected_closure

print("ENTRY_NAME=add")
print("PARAMETERS=x,y")
print("SOURCE_RETURN_AST_MATCHES_CANONICAL=True")
print(f"REGENERATED_MPY_TOKEN_COUNT={len(mpy_tokens)}")
print("CLAIM_LOADALL_PROGRAM_TOKEN_IDENTITY=True")
print("CLAIM_PROGRAM_EXACT_EXPECTED_CONSTRUCTORS=True")
print("FINAL_CLOSURE_BODY_EXACT_EXPECTED_CONSTRUCTORS=True")
print("CLAIM_CALL_ARGUMENTS=Int(X),Int(Y)")
print("CLAIM_RESULT=X +Int Y")
