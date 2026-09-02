#!/usr/bin/env python3
"""Compare macro-expanded proof bodies to the trusted-regenerated MPY constructors."""

from __future__ import annotations

import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/problem-109-independent")
solution = json.loads((SCRATCH / "solution-kast.json").read_text())["term"]
macro_body = json.loads((SCRATCH / "body-kast.json").read_text())["term"]
claim_closure = json.loads((SCRATCH / "closure-kast.json").read_text())["term"]


def label(term: dict) -> str:
    return term["label"]["name"]


assert label(solution) == "Module(_)_MPY-SYNTAX_Module_Stmts"
module_statements = solution["args"][0]
assert label(module_statements) == "___MPY-SYNTAX_Stmts_Stmt_Stmts"
function = module_statements["args"][0]
module_tail = module_statements["args"][1]
assert label(function) == "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
assert function["args"][0]["token"] == '"move_one_ball"'
params = function["args"][1]
assert label(params) == "Params(_)_MPY-SYNTAX_Params_ParamNames"
param_names = params["args"][0]
assert label(param_names) == "_,__MPY-SYNTAX_ParamNames_String_ParamNames"
assert param_names["args"][0]["token"] == '"arr"'
assert not param_names["args"][1].get("args")
assert not module_tail.get("args")

translated_body = function["args"][2]
body_equal = translated_body == macro_body
closure_equal = (
    label(claim_closure) == "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
    and claim_closure["args"][0] == param_names
    and claim_closure["args"][1] == translated_body
    and claim_closure["args"][2]["token"] == "0"
)
print(f"entry_name=move_one_ball")
print(f"parameter_binding=arr")
print(f"module_has_one_function={not module_tail.get('args')}")
print(f"macro_expanded_body_constructor_equal={body_equal}")
print(f"claim_closure_params_body_parent_constructor_equal={closure_equal}")


def find_first(term: dict, prefix: str) -> dict:
    if term.get("node") == "KApply" and label(term).startswith(prefix):
        return term
    for child in term.get("args", []):
        if isinstance(child, dict):
            try:
                return find_first(child, prefix)
            except LookupError:
                pass
    raise LookupError(prefix)


translated_for = find_first(translated_body, "For(")
macro_for = find_first(macro_body, "For(")
loop_body_equal = translated_for["args"][2] == macro_for["args"][2]
print(f"macro_expanded_loop_body_constructor_equal={loop_body_equal}")

if not body_equal or not loop_body_equal or not closure_equal:
    raise SystemExit(1)
