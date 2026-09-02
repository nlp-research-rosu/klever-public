#!/usr/bin/env python3
"""Mechanical constructor comparison of solution.mpy and minPathBody."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path("/tmp/audit-work/129-minPath-audit")


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def flatten_string_list(term: dict) -> list[str]:
    current = term
    values: list[str] = []
    while label(current).startswith("_,__MPY-SYNTAX_ParamNames"):
        head, current = current["args"]
        values.append(head["token"])
    if not label(current).startswith('.List{"_,__MPY-SYNTAX_ParamNames'):
        raise AssertionError(f"unexpected ParamNames tail: {label(current)}")
    return values


def digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    module = json.loads((ROOT / "solution-module.json").read_text())["term"]
    macro_body = json.loads((ROOT / "minpath-body.json").read_text())["term"]
    assert label(module).startswith("Module(_)_MPY-SYNTAX_Module")
    module_statements = module["args"][0]
    function, module_tail = module_statements["args"]
    assert label(function).startswith("FuncDef(_,_,_)")
    name_token, params, translated_body = function["args"]
    assert label(module_tail).startswith('.List{"___MPY-SYNTAX_Stmts')
    assert label(params).startswith("Params(_)")
    param_names = flatten_string_list(params["args"][0])

    spec = (ROOT / "spec.k").read_text()
    target_source_pins_call = 'Call(Name("minPath")' in spec
    target_source_pins_binding = (
        '("minPath" |-> closureVal(("grid", "k", .ParamNames),' in spec
        and "minPathBody, 0))" in spec
    )
    constructor_equal = translated_body == macro_body
    macro_names_remaining = [
        name for name in (
            "minPathBody", "outerLoop", "innerLoop", "upIf", "downIf",
            "leftIf", "rightIf", "resultLoop", "oddTail",
        )
        if name in json.dumps(macro_body)
    ]
    print(f"module_only_one_function={label(module_tail).startswith('.List')}")
    print(f"translated_function_name={name_token['token']}")
    print(f"translated_parameters={param_names}")
    print(f"target_source_pins_call={target_source_pins_call}")
    print(f"target_source_pins_binding={target_source_pins_binding}")
    print(f"macro_names_remaining_after_expansion={macro_names_remaining}")
    print(f"translated_body_sha256={digest(translated_body)}")
    print(f"claim_macro_body_sha256={digest(macro_body)}")
    print(f"constructor_level_body_equal={constructor_equal}")
    if not (
        name_token["token"] == '"minPath"'
        and param_names == ['"grid"', '"k"']
        and target_source_pins_call and target_source_pins_binding
        and not macro_names_remaining and constructor_equal
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
