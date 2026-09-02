#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and the claim closure."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/72-will-it-fly")
DEFINITION = WORK / "reviewer-verification-kompiled"


def run_json(*args: str) -> dict:
    completed = subprocess.run(args, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {args}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return json.loads(completed.stdout)["term"]


program = run_json(
    "kast",
    str(WORK / "solution.mpy"),
    "--definition",
    str(DEFINITION),
    "--output",
    "json",
)

assert program["label"]["name"].startswith("Module(")
module_stmts = program["args"][0]
assert module_stmts["label"]["name"].startswith("___MPY-SYNTAX_Stmts_")
function_def = module_stmts["args"][0]
assert function_def["label"]["name"].startswith("FuncDef(")
name_token, params_wrapper, body_stmts = function_def["args"]
assert name_token["token"] == '"will_it_fly"'
assert params_wrapper["label"]["name"].startswith("Params(")
translated_params = params_wrapper["args"][0]

parsed_definition = (DEFINITION / "parsed.txt").read_text()
matching_rules = [
    line
    for line in parsed_definition.splitlines()
    if line.lstrip().startswith("rule ")
    and "willItFlyClosure()_VERIFICATION-SYNTAX_Val" in line
]
assert len(matching_rules) == 1, len(matching_rules)
rule_text = matching_rules[0]
rhs_kast = rule_text.split("=>", 1)[1].split(" requires ", 1)[0]


def to_kast(term: dict) -> str:
    if term["node"] == "KToken":
        return f'#token({json.dumps(term["token"])},{json.dumps(term["sort"]["name"])})'
    assert term["node"] == "KApply"
    label = term["label"]["name"]
    arguments = ",".join(to_kast(argument) for argument in term["args"])
    if not arguments:
        arguments = ".KList"
    return f"`{label}`({arguments})"


assert rhs_kast.startswith("`closureVal(")
closure_label = rhs_kast[1 : rhs_kast.index("`", 1)]
closure_defining_scope = {
    "node": "KToken",
    "sort": {"node": "KSort", "name": "Int"},
    "token": "0",
}
expected_closure = {
    "node": "KApply",
    "label": {"node": "KLabel", "name": closure_label, "params": []},
    "arity": 3,
    "args": [translated_params, body_stmts, closure_defining_scope],
}
expected_kast = to_kast(expected_closure)
assert rhs_kast == expected_kast

spec_text = (WORK / "spec.k").read_text()
assert spec_text.count('"will_it_fly" |-> willItFlyClosure()') == 4
assert spec_text.count('Call(\n        Name("will_it_fly"),') == 4

print('translated_function_name="will_it_fly"')
print("constructor_params_equal=true")
print("constructor_body_equal=true")
print("closure_defining_scope=0")
print("entry_claim_binding_count=4")
print("entry_claim_call_count=4")
print("REAL_PROGRAM_PINNING=PASS")
