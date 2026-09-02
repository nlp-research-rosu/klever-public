#!/usr/bin/env python3
"""Mechanically compare the submitted FuncDef AST with the proof closure macro."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/26-remove-duplicates/candidate")
DEFINITION = SCRATCH / "verification-kompiled"
SOLUTION = SCRATCH / "solution.mpy"
MODULE = "REMOVE-DUPLICATES-VERIFICATION"


def kast(*extra: str) -> dict:
    command = [
        "kast",
        "--definition",
        str(DEFINITION),
        "--module",
        MODULE,
        "--output",
        "json",
        *extra,
    ]
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stderr:
        print("kast_stderr=" + completed.stderr.strip())
    return json.loads(completed.stdout)["term"]


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def flatten_stmts(term: dict) -> list[dict]:
    result: list[dict] = []
    current = term
    cons_label = "___MPY-SYNTAX_Stmts_Stmt_Stmts"
    empty_prefix = '.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts'
    while label(current) == cons_label:
        result.append(current["args"][0])
        current = current["args"][1]
    if label(current) != empty_prefix:
        raise AssertionError(f"unexpected Stmts tail: {label(current)}")
    return result


def digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    module_term = kast(str(SOLUTION), "--sort", "Module")
    macro_term = kast(
        "--expression",
        "#removeDuplicatesClosure",
        "--sort",
        "Val",
        "--expand-macros",
    )

    if label(module_term) != "Module(_)_MPY-SYNTAX_Module_Stmts":
        raise AssertionError("submitted file is not a Module term")
    module_statements = flatten_stmts(module_term["args"][0])
    if len(module_statements) != 2:
        raise AssertionError(f"unexpected module statement count: {len(module_statements)}")
    import_stmt, function = module_statements
    if not label(import_stmt).startswith("ImportFrom(_,_)_MPY-SYNTAX_Stmt"):
        raise AssertionError("first statement is not ImportFrom")
    if label(function) != "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts":
        raise AssertionError("second statement is not the expected FuncDef")
    if function["args"][0].get("token") != '"remove_duplicates"':
        raise AssertionError("wrong function name")

    expected_closure_label = "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
    if label(macro_term) != expected_closure_label:
        raise AssertionError(f"unexpected macro expansion: {label(macro_term)}")

    function_params_wrapper = function["args"][1]
    if label(function_params_wrapper) != "Params(_)_MPY-SYNTAX_Params_ParamNames":
        raise AssertionError("unexpected Params wrapper")
    function_params = function_params_wrapper["args"][0]
    function_body = function["args"][2]
    macro_params, macro_body, macro_defining_scope = macro_term["args"]

    checks = {
        "parameter_ast_equal": function_params == macro_params,
        "body_ast_equal": function_body == macro_body,
        "macro_defining_scope_is_module_zero": (
            macro_defining_scope.get("token") == "0"
        ),
    }
    print("module_statement_count=2")
    print("function_name=remove_duplicates")
    print(f"function_body_sha256={digest(function_body)}")
    print(f"macro_body_sha256={digest(macro_body)}")
    print(json.dumps(checks, sort_keys=True))
    if not all(checks.values()):
        return 1
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"ERROR={error}")
        sys.exit(1)
