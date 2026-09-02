#!/usr/bin/env python3
"""Check that the proof's solutionClosure macro embeds the submitted MPY body."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def fail(message: str) -> int:
    print(f"PIN_MISMATCH: {message}")
    return 1


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} PARSED_PROGRAM_JSON EXPANDED_CLOSURE_JSON")
        return 64
    program = json.loads(Path(sys.argv[1]).read_text())["term"]
    closure = json.loads(Path(sys.argv[2]).read_text())["term"]

    if not label(program).startswith("Module("):
        return fail(f"program root is {label(program)}")
    stmts = program["args"][0]
    if not label(stmts).startswith("___MPY-SYNTAX_Stmts"):
        return fail(f"module contents are {label(stmts)}")
    func, rest = stmts["args"]
    if not label(rest).startswith(".List{"):
        return fail("submitted module contains more than one top-level statement")
    if not label(func).startswith("FuncDef(_,_,_)"):
        return fail(f"top-level statement is {label(func)}")
    name, params, body = func["args"]
    if name.get("token") != '"solution"':
        return fail(f"function name is {name.get('token')}")
    if not label(params).startswith("Params("):
        return fail(f"function params node is {label(params)}")
    if not label(closure).startswith("closureVal("):
        return fail(f"expanded macro root is {label(closure)}")

    closure_params, closure_body, closure_parent = closure["args"]
    if closure_params != params["args"][0]:
        return fail("parameter list differs")
    if closure_body != body:
        return fail("function body differs")
    if closure_parent.get("token") != "0":
        return fail(f"closure parent is {closure_parent.get('token')}, expected 0")

    print("PIN_CONFIRMED")
    print("module_top_level_statements=1")
    print('function_name="solution"')
    print("parameter_list_matches=true")
    print("function_body_matches=true")
    print("closure_parent_scope=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
