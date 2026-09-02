#!/usr/bin/env python3
"""Constructor-level identity check: solution.mpy versus proof macros."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
DEFINITION = ROOT / "verification-audit-kompiled"


def kast_file(path: Path, sort: str) -> dict:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--sort",
        sort,
        "--expand-macros",
        "--output",
        "json",
    ]
    return json.loads(subprocess.check_output(command, cwd=ROOT, text=True))["term"]


def kast_expression(expression: str, sort: str) -> dict:
    command = [
        "kast",
        "--expression",
        expression,
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--sort",
        sort,
        "--expand-macros",
        "--output",
        "json",
    ]
    return json.loads(subprocess.check_output(command, cwd=ROOT, text=True))["term"]


def label(term: dict) -> str:
    return term["label"]["name"]


def canonical_hash(term: dict) -> str:
    data = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


module = kast_file(ROOT / "solution.mpy", "Module")
body_macro = kast_expression("solutionBody", "Stmts")
closure_macro = kast_expression("solutionClosure", "Val")

assert label(module) == "Module(_)_MPY-SYNTAX_Module_Stmts"
module_stmts = module["args"][0]
assert label(module_stmts) == "___MPY-SYNTAX_Stmts_Stmt_Stmts"
function = module_stmts["args"][0]
module_tail = module_stmts["args"][1]
assert label(function) == "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
assert label(module_tail).startswith('.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}')
name, params, emitted_body = function["args"]
assert name["token"] == '"solution"'

assert label(closure_macro) == "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
closure_params, closure_body, closure_environment = closure_macro["args"]
assert closure_environment["token"] == "0"

print("module_has_exactly_one_statement:", True)
print("module_statement_is_solution_funcdef:", True)
print("emitted_body_equals_expanded_solutionBody:", emitted_body == body_macro)
print("closure_body_equals_emitted_body:", closure_body == emitted_body)
print("closure_params_equal_funcdef_params:", closure_params == params["args"][0])
print("closure_environment:", closure_environment["token"])
print("emitted_body_kast_sha256:", canonical_hash(emitted_body))
print("expanded_solutionBody_kast_sha256:", canonical_hash(body_macro))
print("expanded_solutionClosure_body_kast_sha256:", canonical_hash(closure_body))

assert emitted_body == body_macro
assert closure_body == emitted_body
assert closure_params == params["args"][0]
print("program_pinning_status: PASS")
