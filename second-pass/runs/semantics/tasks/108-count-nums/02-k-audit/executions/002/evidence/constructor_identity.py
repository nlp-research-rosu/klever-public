#!/usr/bin/env python3
"""Mechanically compare submitted module constructors with proof claim macros."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
DEFINITION = ROOT / "audit-loop-base-kompiled"
MODULE = "COUNT-NUMS-VERIFICATION-BASE"


def kast_file(path: Path, sort: str) -> dict:
    command = [
        "kast", str(path), "--definition", str(DEFINITION),
        "--sort", sort, "--output", "json", "--expand-macros",
    ]
    return json.loads(subprocess.check_output(command, cwd=ROOT, text=True))["term"]


def kast_expr(expression: str, sort: str) -> dict:
    command = [
        "kast", "--definition", str(DEFINITION), "--module", MODULE,
        "--sort", sort, "--expression", expression,
        "--output", "json", "--expand-macros",
    ]
    return json.loads(subprocess.check_output(command, cwd=ROOT, text=True))["term"]


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def walk(term: object):
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


solution = kast_file(ROOT / "solution.mpy", "Module")
functions: dict[str, tuple[dict, dict]] = {}
for term in walk(solution):
    if label(term).startswith("FuncDef(_,_,_)"):
        name_term, params_term, body_term = term["args"]
        name = json.loads(name_term["token"])
        functions[name] = (params_term["args"][0], body_term)

expected = {
    "positive_digit_sum": ("positiveFunctionBody", "positiveDigitClosure"),
    "negative_digit_sum": ("negativeFunctionBody", "negativeDigitClosure"),
    "signed_digit_sum": ("signedFunctionBody", "signedDigitClosure"),
    "count_nums": ("countFunctionBody", "countNumsClosure"),
}
assert set(functions) == set(expected)

closures: dict[str, dict] = {}
for function_name, (body_macro, closure_macro) in expected.items():
    params, submitted_body = functions[function_name]
    proof_body = kast_expr(body_macro, "Stmts")
    proof_closure = kast_expr(closure_macro, "Val")
    assert submitted_body == proof_body
    assert label(proof_closure).startswith("closureVal(_,_,_)")
    closure_params, closure_body, closure_env = proof_closure["args"]
    assert closure_params == params
    assert closure_body == submitted_body
    assert closure_env["token"] == "0"
    closures[function_name] = proof_closure
    print(
        f"FUNCTION {function_name}: body_macro={body_macro} exact=true "
        f"closure_macro={closure_macro} params_exact=true env=0"
    )

bindings = kast_expr("digitFunctionBindings", "Map")
map_items: dict[str, dict] = {}
for term in walk(bindings):
    if "|->_" in label(term) and len(term.get("args", [])) == 2:
        key, value = term["args"]
        if key.get("node") == "KToken" and key.get("sort", {}).get("name") == "String":
            map_items[json.loads(key["token"])] = value

expected_helpers = {
    name: closures[name]
    for name in ("positive_digit_sum", "negative_digit_sum", "signed_digit_sum")
}
assert map_items == expected_helpers
print(f"DIGIT_BINDINGS keys={sorted(map_items)} exact_closures=true")
print("COUNT_ENTRY_DIRECT_CLOSURE=countNumsClosure")
print("CONSTRUCTOR_IDENTITY=PASS")
