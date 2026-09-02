#!/usr/bin/env python3
"""Constructor-level comparison of the translated function and proof macro."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")


def run_kast(*arguments: str) -> dict:
    completed = subprocess.run(
        ["kast", *arguments],
        cwd=WORK,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


solution = run_kast(
    "--definition",
    "runtime-kompiled",
    "--module",
    "MPY-SYNTAX",
    "--sort",
    "Module",
    "--output",
    "json",
    "solution.regenerated.mpy",
)
macro = run_kast(
    "--definition",
    "verification-kompiled",
    "--module",
    "VERIFICATION",
    "--sort",
    "Stmts",
    "--expand-macros",
    "--output",
    "json",
    "--expression",
    "numericalLetterGradeBody",
)

module_term = solution["term"]
assert module_term["label"]["name"] == "Module(_)_MPY-SYNTAX_Module_Stmts"
module_stmts = module_term["args"][0]
assert module_stmts["label"]["name"] == "___MPY-SYNTAX_Stmts_Stmt_Stmts"
function = module_stmts["args"][0]
module_tail = module_stmts["args"][1]
assert function["label"]["name"] == "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
assert function["args"][0]["token"] == '"numerical_letter_grade"'

params = function["args"][1]
params_text = json.dumps(params, sort_keys=True, separators=(",", ":"))
param_head = params["args"][0]
assert param_head["args"][0]["token"] == '"grades"'
assert param_head["args"][1]["arity"] == 0
assert "_,__MPY-SYNTAX_ParamNames_String_ParamNames" in params_text

assert module_tail["arity"] == 0
assert "Stmts" in module_tail["label"]["name"]
translated_body = function["args"][2]
expanded_macro_body = macro["term"]

translated_bytes = json.dumps(
    translated_body, sort_keys=True, separators=(",", ":")
).encode()
macro_bytes = json.dumps(
    expanded_macro_body, sort_keys=True, separators=(",", ":")
).encode()

print("TRANSLATED_ENTRY=numerical_letter_grade")
print("TRANSLATED_PARAMS=grades")
print("TRANSLATED_MODULE_EXTRA_STATEMENTS=0")
print(f"TRANSLATED_BODY_SHA256={hashlib.sha256(translated_bytes).hexdigest()}")
print(f"EXPANDED_MACRO_BODY_SHA256={hashlib.sha256(macro_bytes).hexdigest()}")
print(f"CONSTRUCTOR_BODY_EQUAL={translated_body == expanded_macro_body}")
if translated_body != expanded_macro_body:
    raise SystemExit(1)

verification_text = (WORK / "verification.k").read_text(encoding="utf-8")
needle = (
    'toCall(closureVal("grades", numericalLetterGradeBody, 0))'
)
print(f"RUNGRADES_BINDS_EXPANDED_BODY={needle in verification_text}")
if needle not in verification_text:
    raise SystemExit(1)

print("PINNING_COMPARE_OK")
