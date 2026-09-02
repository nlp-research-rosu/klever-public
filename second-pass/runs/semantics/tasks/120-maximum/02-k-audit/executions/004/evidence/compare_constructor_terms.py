#!/usr/bin/env python3
"""Mechanically compare the submitted function body with maximumBody."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")


def label(term: dict) -> str:
    return term["label"]["name"]


solution = json.loads((EVIDENCE / "solution-expanded-kast.json").read_text())["term"]
macro_body = json.loads(
    (EVIDENCE / "maximumBody-expanded-kast.json").read_text()
)["term"]

assert label(solution) == "Module(_)_MPY-SYNTAX_Module_Stmts"
module_stmts = solution["args"][0]
assert label(module_stmts) == "___MPY-SYNTAX_Stmts_Stmt_Stmts"
function = module_stmts["args"][0]
module_tail = module_stmts["args"][1]
assert (
    label(module_tail)
    == '.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts'
)
assert label(function) == "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
name, params, submitted_body = function["args"]
assert name["token"] == '"maximum"'
assert label(params) == "Params(_)_MPY-SYNTAX_Params_ParamNames"

param_names: list[str] = []
cursor = params["args"][0]
while label(cursor) == "_,__MPY-SYNTAX_ParamNames_String_ParamNames":
    token, cursor = cursor["args"]
    param_names.append(json.loads(token["token"]))
assert label(cursor) == '.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames'
assert param_names == ["arr", "k"]

submitted_canonical = json.dumps(
    submitted_body, sort_keys=True, separators=(",", ":")
).encode()
macro_canonical = json.dumps(macro_body, sort_keys=True, separators=(",", ":")).encode()

print("module_function_count=1")
print("function_name=maximum")
print(f"parameters={param_names!r}")
print("submitted_body_sha256=" + hashlib.sha256(submitted_canonical).hexdigest())
print("maximumBody_sha256=" + hashlib.sha256(macro_canonical).hexdigest())
print(f"constructor_terms_equal={submitted_body == macro_body}")
assert submitted_body == macro_body
