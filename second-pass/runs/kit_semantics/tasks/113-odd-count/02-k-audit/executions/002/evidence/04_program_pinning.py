#!/usr/bin/env python3
"""Constructor-level comparison of submitted mpy and claim-body macros."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def term(path: str) -> dict:
    return json.loads(Path(path).read_text())["term"]


def label(value: dict) -> str:
    return value["label"]["name"]


def canonical_hash(value: dict) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def statements(value: dict) -> list[dict]:
    result = []
    current = value
    cons = "___MPY-SYNTAX_Stmts_Stmt_Stmts"
    empty = '.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts'
    while label(current) == cons:
        result.append(current["args"][0])
        current = current["args"][1]
    assert label(current) == empty, label(current)
    return result


solution = term("/audit-output/evidence/04_solution.kast.json")
macro_body = term("/audit-output/evidence/04_body.kast.json")
macro_loop = term("/audit-output/evidence/04_loop.kast.json")

assert label(solution) == "Module(_)_MPY-SYNTAX_Module_Stmts"
module_statements = statements(solution["args"][0])
assert len(module_statements) == 1
function = module_statements[0]
assert label(function) == "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"

name, params, translated_body = function["args"]
assert name["node"] == "KToken" and name["token"] == '"odd_count"'
assert label(params) == "Params(_)_MPY-SYNTAX_Params_ParamNames"
parameter_entries = params["args"][0]
assert label(parameter_entries) == "_,__MPY-SYNTAX_ParamNames_String_ParamNames"
parameter = parameter_entries["args"][0]
assert parameter["node"] == "KToken" and parameter["token"] == '"lst"'

body_equal = translated_body == macro_body
body_statements = statements(translated_body)
for_statements = [
    statement
    for statement in body_statements
    if label(statement) == "For(_,_,_)_MPY-SYNTAX_Stmt_Expr_Expr_Stmts"
]
assert len(for_statements) == 1
translated_loop = for_statements[0]["args"][2]
loop_equal = translated_loop == macro_loop

print('FUNCTION_NAME="odd_count"')
print('PARAMETER_NAME="lst"')
print(f"MODULE_TOP_LEVEL_STATEMENTS={len(module_statements)}")
print(f"FUNCTION_BODY_STATEMENTS={len(body_statements)}")
print(f"BODY_CONSTRUCTOR_SHA256={canonical_hash(translated_body)}")
print(f"MACRO_BODY_CONSTRUCTOR_SHA256={canonical_hash(macro_body)}")
print(f"BODY_CONSTRUCTOR_EQUAL={body_equal}")
print(f"LOOP_CONSTRUCTOR_SHA256={canonical_hash(translated_loop)}")
print(f"MACRO_LOOP_CONSTRUCTOR_SHA256={canonical_hash(macro_loop)}")
print(f"LOOP_CONSTRUCTOR_EQUAL={loop_equal}")

raise SystemExit(0 if body_equal and loop_equal else 1)
