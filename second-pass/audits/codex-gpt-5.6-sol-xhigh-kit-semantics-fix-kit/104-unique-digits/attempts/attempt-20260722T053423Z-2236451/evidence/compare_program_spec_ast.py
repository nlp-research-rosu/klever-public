#!/usr/bin/env python3
"""Compare the parsed submitted FuncDef with the closure pinned by the entry claim."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterator


FUNC_LABEL = "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
CLOSURE_LABEL = "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
PARAMS_LABEL = "Params(_)_MPY-SYNTAX_Params_ParamNames"


def walk(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def label(node: dict[str, Any]) -> str | None:
    raw = node.get("label")
    return raw.get("name") if isinstance(raw, dict) else None


def applications(root: Any, wanted: str) -> list[dict[str, Any]]:
    return [node for node in walk(root) if node.get("node") == "KApply" and label(node) == wanted]


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} SOLUTION_KAST.json SPEC_KAST.json", file=sys.stderr)
        return 64
    solution = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    spec = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    functions = applications(solution, FUNC_LABEL)
    closures = applications(spec, CLOSURE_LABEL)
    print(f"PARSED_FUNCDEFS: {len(functions)}")
    print(f"SPEC_CLOSURES: {len(closures)}")
    if len(functions) != 1:
        print("ERROR: submitted module does not contain exactly one plain FuncDef")
        return 1
    function = functions[0]
    function_args = function["args"]
    params_node = function_args[1]
    if label(params_node) != PARAMS_LABEL:
        print("ERROR: unexpected Params node")
        return 1
    function_name = function_args[0]
    function_params = params_node["args"][0]
    function_body = function_args[2]
    matches = []
    for closure in closures:
        closure_params, closure_body, closure_env = closure["args"]
        name_is_unique_digits = function_name.get("token") == '"unique_digits"'
        params_equal = closure_params == function_params
        body_equal = closure_body == function_body
        env_is_module = closure_env.get("node") == "KToken" and closure_env.get("token") == "0"
        if name_is_unique_digits and params_equal and body_equal and env_is_module:
            matches.append(closure)
    print(f"EXACT_ENTRY_CLOSURE_MATCHES: {len(matches)}")
    print(f"FUNCTION_NAME_TOKEN: {function_name.get('token')}")
    print("PARAMETERS_EQUAL: " + ("true" if matches else "false"))
    print("BODY_EQUAL: " + ("true" if matches else "false"))
    print("DEFINITION_ENVIRONMENT_ZERO: " + ("true" if matches else "false"))
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
