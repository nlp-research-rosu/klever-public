#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and the claim closure."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate-scratch")
DEFINITION = WORK / "audit-verification-kompiled"


def kast(*arguments: str) -> dict:
    completed = subprocess.run(
        ["kast", "--definition", str(DEFINITION), *arguments, "--output", "json"],
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    document = json.loads(completed.stdout)
    return document["term"]


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def flatten_stmts(term: dict) -> list[dict]:
    if term.get("arity") == 0 and label(term).startswith(".List{"):
        return []
    assert "Stmts_Stmt_Stmts" in label(term), label(term)
    assert term["arity"] == 2
    return [term["args"][0], *flatten_stmts(term["args"][1])]


def main() -> None:
    module = kast(
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        str(WORK / "solution.mpy"),
    )
    assert label(module).startswith("Module(")
    statements = flatten_stmts(module["args"][0])
    assert len(statements) == 2, "module must contain only inert typing import and target def"

    imported, function = statements
    assert label(imported).startswith("ImportFrom(")
    assert imported["args"][0]["token"] == '"typing"'
    imported_names = imported["args"][1]
    assert "ParamNames_String_ParamNames" in label(imported_names)
    assert imported_names["args"][0]["token"] == '"List"'
    assert imported_names["args"][1]["arity"] == 0

    assert label(function).startswith("FuncDef(")
    assert function["args"][0]["token"] == '"remove_duplicates"'
    params_wrapper = function["args"][1]
    assert label(params_wrapper).startswith("Params(")
    translated_params = params_wrapper["args"][0]
    translated_body = function["args"][2]

    claim_closure = kast(
        "--module",
        "REMOVE-DUPLICATES-VERIFICATION",
        "--sort",
        "Val",
        "--expression",
        "#removeDuplicatesClosure",
        "--expand-macros",
    )
    assert label(claim_closure).startswith("closureVal(")
    closure_params, closure_body, closure_environment = claim_closure["args"]

    assert closure_params == translated_params
    assert closure_body == translated_body
    assert closure_environment["token"] == "0"
    assert closure_environment["sort"]["name"] == "Int"

    print("solution_module_statements: inert ImportFrom('typing','List') + target FuncDef")
    print("target_binding: remove_duplicates")
    print("constructor_params_equal: true")
    print("constructor_body_equal: true")
    print("definition_environment_equal: module scope 0")
    print("program_pinning: PASS")


if __name__ == "__main__":
    main()
