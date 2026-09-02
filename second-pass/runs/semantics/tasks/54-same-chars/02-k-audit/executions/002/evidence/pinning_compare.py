#!/usr/bin/env python3
"""Mechanically compare solution.mpy's function constructors with the proof launcher."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/54-same-chars")
DEFINITION = WORK / "audit-verification-kompiled"


def kast(*arguments: str) -> dict:
    command = ["kast", *arguments, "--definition", str(DEFINITION), "--output", "json"]
    result = subprocess.run(command, cwd=WORK, check=True, text=True, capture_output=True)
    return json.loads(result.stdout)["term"]


def label(term: dict) -> str:
    return term["label"]["name"]


def expect_label(term: dict, prefix: str) -> None:
    actual = label(term)
    if not actual.startswith(prefix):
        raise AssertionError(f"expected label prefix {prefix!r}, got {actual!r}")


def collect_name_tokens(term: object, names: list[str]) -> None:
    if isinstance(term, dict):
        if term.get("node") == "KApply" and label(term).startswith("Name(_)"):
            names.append(term["args"][0]["token"])
        for value in term.values():
            collect_name_tokens(value, names)
    elif isinstance(term, list):
        for value in term:
            collect_name_tokens(value, names)


source = kast(
    "solution.mpy",
    "--module",
    "MPY-SYNTAX",
    "--sort",
    "Module",
)
expect_label(source, "Module(_)")
source_stmts = source["args"][0]
expect_label(source_stmts, "___MPY-SYNTAX_Stmts")
function = source_stmts["args"][0]
source_tail = source_stmts["args"][1]
expect_label(function, "FuncDef(_,_,_)")
expect_label(source_tail, ".List{")
function_name, params_wrapper, source_body = function["args"]
expect_label(params_wrapper, "Params(_)")
source_params = params_wrapper["args"][0]

verification_text = (WORK / "verification.k").read_text()
match = re.search(
    r"(?ms)^\s*rule\s+(<k>\s*#sameChars.*?</k>)",
    verification_text,
)
if match is None:
    raise AssertionError("could not extract #sameChars rule")
rule_term = kast(
    "--expression",
    match.group(1),
    "--module",
    "SAME-CHARS-VERIFICATION",
    "--input",
    "rule",
)
expect_label(rule_term, "<k>")
rewrite = rule_term["args"][0]["items"][0]
if rewrite["node"] != "KRewrite":
    raise AssertionError("the first k-sequence item is not a rewrite")
expect_label(rewrite["lhs"], "#sameChars(_,_)")
launch_call = rewrite["rhs"]
expect_label(launch_call, "Call(_,_)")
closure, actual_args = launch_call["args"]
expect_label(closure, "closureVal(_,_,_)")
proof_params, proof_body, captured_env = closure["args"]

if function_name["token"] != '"same_chars"':
    raise AssertionError(f"wrong function binding: {function_name}")
if source_params != proof_params:
    raise AssertionError("parameter constructor tree differs")
if source_body != proof_body:
    raise AssertionError("function-body constructor tree differs")
if captured_env.get("token") != "0":
    raise AssertionError(f"proof closure captures unexpected environment: {captured_env}")

expect_label(actual_args, "_,__MPY-SYNTAX_Exprs")
first_arg, remaining_args = actual_args["args"]
second_arg, args_tail = remaining_args["args"]
expect_label(first_arg, "str(_)")
expect_label(second_arg, "str(_)")
if first_arg["args"][0].get("name") != "S0":
    raise AssertionError("first actual argument is not str(S0)")
if second_arg["args"][0].get("name") != "S1":
    raise AssertionError("second actual argument is not str(S1)")
expect_label(args_tail, ".List{")

name_tokens: list[str] = []
collect_name_tokens(source_body, name_tokens)

print('function_binding="same_chars"')
print("parameter_constructor_identity=true")
print("body_constructor_identity=true")
print("captured_environment=0")
print("argument_mapping=(s0<-str(S0),s1<-str(S1))")
print(f"body_Name_tokens={name_tokens!r}")
print('self_name_lookup_in_body=false' if '"same_chars"' not in name_tokens else 'self_name_lookup_in_body=true')
print("mechanical_pinning_result=PASS")
