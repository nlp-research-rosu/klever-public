#!/usr/bin/env python3
"""Mechanical KAST comparison of translated FuncDef and claimed closure."""

from __future__ import annotations

import json
from pathlib import Path


def label(term: dict) -> str:
    return term["label"]["name"]


def main() -> int:
    root = Path("/tmp/audit-work/reconstruction")
    module = json.loads((root / "solution.ast.json").read_text())["term"]
    closure = json.loads((root / "closure.ast.json").read_text())["term"]
    assert label(module).startswith("Module(")
    statements = module["args"][0]
    assert label(statements).startswith("___MPY-SYNTAX_Stmts")
    import_from, statements = statements["args"]
    assert label(import_from).startswith("ImportFrom(")
    assert import_from["args"][0]["token"] == '"typing"'
    imported_names = import_from["args"][1]
    assert imported_names["args"][0]["token"] == '"List"'
    function, empty_statements = statements["args"]
    assert label(function).startswith("FuncDef(")
    assert function["args"][0]["token"] == '"separate_paren_groups"'
    assert not empty_statements["args"]
    params_wrapper = function["args"][1]
    translated_params = params_wrapper["args"][0]
    translated_body = function["args"][2]
    assert label(closure).startswith("closureVal(")
    claimed_params, claimed_body, defining_env = closure["args"]
    print(f"entry_name={function['args'][0]['token']}")
    print(f"typing_import={import_from['args'][0]['token']} List")
    print(f"defining_env={defining_env['token']}")
    print(f"parameter_kast_equal={translated_params == claimed_params}")
    print(f"body_kast_equal={translated_body == claimed_body}")
    assert defining_env["token"] == "0"
    assert translated_params == claimed_params
    assert translated_body == claimed_body
    print("PROGRAM_TERM_PINNED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
