#!/usr/bin/env python3
"""Mechanical constructor-level pinning check for the submitted function."""

from __future__ import annotations

import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/150-x-or-y-review")


def term(name: str) -> dict:
    return json.loads((SCRATCH / name).read_text())["term"]


def label(node: dict) -> str:
    return node["label"]["name"]


def names(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        if node.get("node") == "KApply" and str(
            node.get("label", {}).get("name", "")
        ).startswith("Name(_)_"):
            found.append(node["args"][0]["token"].strip('"'))
        for value in node.values():
            found.extend(names(value))
    elif isinstance(node, list):
        for value in node:
            found.extend(names(value))
    return found


def main() -> int:
    module = term("solution.kast.json")
    macro_body = term("macro-body.kast.json")
    entry = term("entry.kast.json")

    assert label(module) == "Module(_)_MPY-SYNTAX_Module_Stmts"
    top_stmts = module["args"][0]
    assert label(top_stmts) == "___MPY-SYNTAX_Stmts_Stmt_Stmts"
    function, module_rest = top_stmts["args"]
    assert label(module_rest).startswith(".List{")
    assert label(function) == "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
    function_name, params_wrapper, translated_body = function["args"]
    assert function_name["token"] == '"x_or_y"'
    translated_params = params_wrapper["args"][0]

    assert label(entry) == "Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs"
    closure, call_args = entry["args"]
    assert label(closure) == "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
    closure_params, closure_body, defining_env = closure["args"]

    checks = {
        "only one top-level translated statement": label(module_rest).startswith(".List{"),
        "translated function name is x_or_y": function_name["token"] == '"x_or_y"',
        "entry closure parameter list equals translated parameter list": (
            closure_params == translated_params
        ),
        "macro-expanded xOrYBody equals translated function body": (
            macro_body == translated_body
        ),
        "entry closure body equals translated function body": (
            closure_body == translated_body
        ),
        "entry closure defining environment is module scope 0": (
            defining_env.get("token") == "0"
        ),
    }

    call_arg_tokens: list[str] = []
    cursor = call_args
    while label(cursor) == "_,__MPY-SYNTAX_Exprs_Expr_Exprs":
        head, cursor = cursor["args"]
        call_arg_tokens.append(head["token"])
    checks["ground entry parse preserved arguments 7,34,12"] = (
        call_arg_tokens == ["7", "34", "12"]
    )
    body_names = sorted(set(names(translated_body)))
    checks["body does not read its own module binding x_or_y"] = (
        "x_or_y" not in body_names
    )
    checks["only free nonlocal name is range"] = (
        set(body_names) - {"n", "x", "y", "divisor"} == {"range"}
    )

    for description, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} {description}")
    print(f"translated_body_json_bytes={len(json.dumps(translated_body, sort_keys=True))}")
    print(f"macro_body_json_bytes={len(json.dumps(macro_body, sort_keys=True))}")
    print(f"body_name_tokens={body_names}")
    ok = all(checks.values())
    print(f"OVERALL {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
