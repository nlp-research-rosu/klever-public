#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and proof macros."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path("/tmp/audit-work/src")


def load_term(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text())["term"]


def label(term: dict[str, Any]) -> str:
    return term["label"]["name"]


def token(term: dict[str, Any]) -> str:
    assert term["node"] == "KToken"
    return json.loads(term["token"])


def find_funcdefs(term: dict[str, Any]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}

    def visit(node: Any) -> None:
        if not isinstance(node, dict):
            return
        if node.get("node") == "KApply":
            if label(node).startswith("FuncDef("):
                name = token(node["args"][0])
                found[name] = node
            for child in node.get("args", []):
                visit(child)

    visit(term)
    return found


def canonical_sha(term: Any) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def assert_closure_matches(
    function: dict[str, Any],
    closure: dict[str, Any],
    function_name: str,
) -> None:
    assert label(function).startswith("FuncDef(")
    assert label(closure).startswith("closureVal(")
    function_params = function["args"][1]
    assert label(function_params).startswith("Params(")
    function_param_names = function_params["args"][0]
    function_body = function["args"][2]
    closure_param_names, closure_body, closure_env = closure["args"]
    assert function_param_names == closure_param_names
    assert function_body == closure_body
    assert token(closure_env) == 0
    print(
        f"{function_name}: params_sha256={canonical_sha(function_param_names)} "
        f"body_sha256={canonical_sha(function_body)} exact_match=true"
    )


def main() -> None:
    module = load_term("solution-module.json")
    assert label(module).startswith("Module(")
    functions = find_funcdefs(module)
    assert set(functions) == {"_column_desc", "_row_asc", "get_row"}

    getrow_macro = load_term("getrowbody-expanded.json")
    getrow_body = functions["get_row"]["args"][2]
    assert getrow_body == getrow_macro
    print(
        "get_row: "
        f"body_sha256={canonical_sha(getrow_body)} exact_macro_match=true"
    )

    assert_closure_matches(
        functions["_column_desc"],
        load_term("columnclosure-expanded.json"),
        "_column_desc",
    )
    assert_closure_matches(
        functions["_row_asc"],
        load_term("rowclosure-expanded.json"),
        "_row_asc",
    )
    print("ALL_THREE_SUBMITTED_FUNCTION_BODIES_PINNED")


if __name__ == "__main__":
    main()
