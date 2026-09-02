#!/usr/bin/env python3
"""Mechanically compare the submitted function body with proof macro terms."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def is_list_cons(term: dict, sort_name: str) -> bool:
    term_label = label(term)
    return (
        term.get("node") == "KApply"
        and term.get("arity") == 2
        and f"MPY-SYNTAX_{sort_name}_" in term_label
    )


def is_list_nil(term: dict, sort_name: str) -> bool:
    return (
        term.get("node") == "KApply"
        and term.get("arity") == 0
        and f"_{sort_name}" in label(term)
        and label(term).startswith(".List")
    )


def flatten_list(term: dict, sort_name: str) -> list[dict]:
    items: list[dict] = []
    current = term
    while is_list_cons(current, sort_name):
        items.append(current["args"][0])
        current = current["args"][1]
    if not is_list_nil(current, sort_name):
        raise AssertionError(f"unexpected {sort_name} tail: {label(current)}")
    return items


def load_term(path: Path) -> dict:
    return json.loads(path.read_text())["term"]


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: constructor_compare.py SOLUTION.json ENTRY.json COND.json LOOP.json"
        )
    solution, entry, condition, loop = map(lambda p: load_term(Path(p)), sys.argv[1:])

    assert label(solution).startswith("Module(_)")
    module_statements = flatten_list(solution["args"][0], "Stmts")
    assert len(module_statements) == 1
    function = module_statements[0]
    assert label(function).startswith("FuncDef(_,_,_)")
    assert function["args"][0]["token"] == '"is_prime"'
    params = flatten_list(function["args"][1]["args"][0], "ParamNames")
    assert [item["token"] for item in params] == ['"n"']
    submitted_body = function["args"][2]

    body_equal = submitted_body == entry
    body_statements = flatten_list(submitted_body, "Stmts")
    assert len(body_statements) == 4
    while_statement = body_statements[2]
    assert label(while_statement).startswith("While(_,_)")
    condition_equal = while_statement["args"][0] == condition
    loop_equal = while_statement["args"][1] == loop

    print(f"function_name={function['args'][0]['token']}")
    print(f"parameters={[item['token'] for item in params]}")
    print(f"body_statement_count={len(body_statements)}")
    print(f"entry_macro_equals_submitted_body={body_equal}")
    print(f"condition_macro_equals_submitted_while_condition={condition_equal}")
    print(f"loop_macro_equals_submitted_while_body={loop_equal}")
    if not (body_equal and condition_equal and loop_equal):
        return 1
    print("RESULT: constructor-level identity established")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
