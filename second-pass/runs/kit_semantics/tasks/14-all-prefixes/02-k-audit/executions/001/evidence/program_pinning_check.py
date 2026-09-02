#!/usr/bin/env python3
"""Mechanical constructor-level comparison of regenerated program and K claim."""

from __future__ import annotations

import json
from typing import Any, Iterator


SOLUTION_JSON = "/tmp/audit-work/solution-kast.json"
SPEC_JSON = "/tmp/audit-work/spec-emitted.json"


def label(term: dict[str, Any]) -> str | None:
    if term.get("node") != "KApply":
        return None
    return term["label"]["name"]


def walk(term: Any) -> Iterator[dict[str, Any]]:
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def claim_label(claim: dict[str, Any]) -> str | None:
    return claim.get("att", {}).get("att", {}).get("label")


def only(items: list[Any], description: str) -> Any:
    assert len(items) == 1, f"{description}: expected one, got {len(items)}"
    return items[0]


def flatten_stmts(term: dict[str, Any]) -> list[dict[str, Any]]:
    cons = "___MPY-SYNTAX_Stmts_Stmt_Stmts"
    empty = '.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts'
    result = []
    cursor = term
    while label(cursor) == cons:
        result.append(cursor["args"][0])
        cursor = cursor["args"][1]
    assert label(cursor) == empty, f"unexpected Stmts tail: {label(cursor)}"
    return result


def token(term: dict[str, Any]) -> str:
    assert term["node"] == "KToken"
    return json.loads(term["token"])


def main() -> None:
    solution = json.load(open(SOLUTION_JSON, encoding="utf-8"))["term"]
    spec = json.load(open(SPEC_JSON, encoding="utf-8"))["term"]

    modules = spec["term"]
    spec_module = only([module for module in modules if module["name"] == "SPEC"], "SPEC module")
    target = only(
        [
            sentence
            for sentence in spec_module["localSentences"]
            if sentence["node"] == "KClaim" and claim_label(sentence) == "SPEC.all-prefixes"
        ],
        "SPEC.all-prefixes claim",
    )

    load_calls = [
        term
        for term in walk(target["body"])
        if label(term) == "#loadAll(_)_MPY-CORE_KItem_Module"
    ]
    load_call = only(load_calls, "#loadAll term")
    claim_module = load_call["args"][0]
    assert label(solution) == "Module(_)_MPY-SYNTAX_Module_Stmts"
    assert label(claim_module) == label(solution)

    solution_statements = flatten_stmts(solution["args"][0])
    claim_statements = flatten_stmts(claim_module["args"][0])
    assert len(solution_statements) == 2
    assert len(claim_statements) == 3
    assert claim_statements[:2] == solution_statements
    print("regenerated_Module_prefix_equals_claim_Module: PASS (2 exact statements)")

    suffix = claim_statements[2]
    assert label(suffix) == "Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr"
    lhs, rhs = suffix["args"]
    assert label(lhs) == "Name(_)_MPY-SYNTAX_Expr_String"
    assert token(lhs["args"][0]) == "result"
    assert label(rhs) == "Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs"
    callee, arguments = rhs["args"]
    assert label(callee) == "Name(_)_MPY-SYNTAX_Expr_String"
    assert token(callee["args"][0]) == "all_prefixes"
    argument_items = []
    cursor = arguments
    expr_cons = "_,__MPY-SYNTAX_Exprs_Expr_Exprs"
    expr_empty = '.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs'
    while label(cursor) == expr_cons:
        argument_items.append(cursor["args"][0])
        cursor = cursor["args"][1]
    assert label(cursor) == expr_empty and len(argument_items) == 1
    assert label(argument_items[0]) == "Name(_)_MPY-SYNTAX_Expr_String"
    assert token(argument_items[0]["args"][0]) == "input"
    print("claim_only_suffix: PASS result = all_prefixes(input)")

    function = solution_statements[1]
    assert label(function) == "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
    assert token(function["args"][0]) == "all_prefixes"
    closures = [
        term
        for term in walk(target["body"])
        if label(term) == "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
    ]
    closure = only(closures, "target destination closure")
    params_wrapper = function["args"][1]
    assert label(params_wrapper) == "Params(_)_MPY-SYNTAX_Params_ParamNames"
    assert closure["args"][0] == params_wrapper["args"][0]
    assert closure["args"][1] == function["args"][2]
    assert token(closure["args"][2]) == 0
    print("destination_closure_binding_and_body: PASS exact constructor identity")

    prefixes_summaries = [
        term for term in walk(target["body"]) if (label(term) or "").startswith("prefixesAcc(")
    ]
    summary = only(prefixes_summaries, "target prefixesAcc postcondition")
    assert label(summary["args"][0]) == ".IntSeq_MPY-CORE_IntSeq"
    assert summary["args"][1]["node"] == "KVariable"
    assert summary["args"][1]["name"] == "INPUT"
    assert label(summary["args"][2]) == ".ValSeq_MPY-CORE_ValSeq"
    print("result_postcondition: PASS list(prefixesAcc(.IntSeq, INPUT, .ValSeq))")

    print("satisfying_entry_witness: INPUT=iCons(97,iCons(98,iCons(99,.IntSeq))) ('abc')")
    print("claimed_witness_result: ['a', 'ab', 'abc']")


if __name__ == "__main__":
    main()
