#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and proof terms."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "audit-verification-kompiled"
VERIFICATION = WORK / "verification.k"


def run_kast_file(path: Path) -> dict:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--output",
        "json",
    ]
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    return json.loads(result.stdout)["term"]


def run_kast_expression(expression: str, sort: str) -> dict:
    # The K rule parser spells empty generated lists as .Stmts/.Exprs, while
    # the program parser represents them by an empty list between delimiters.
    expression = expression.replace(".Stmts", "").replace(".Exprs", "")
    command = [
        "kast",
        "--expression",
        expression,
        "--sort",
        sort,
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--output",
        "json",
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(
            f"kast failed ({result.returncode})\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return json.loads(result.stdout)["term"]


def label(term: dict) -> str:
    if term.get("node") != "KApply":
        return ""
    return term["label"]["name"]


def flatten_list(term: dict, sort_marker: str) -> list[dict]:
    name = label(term)
    if name.startswith(".List{") and name.endswith(f"}}_{sort_marker}"):
        return []
    if sort_marker == "Stmts" and "Stmts_Stmt_Stmts" in name:
        return [term["args"][0], *flatten_list(term["args"][1], sort_marker)]
    if sort_marker == "ParamNames" and "ParamNames_String_ParamNames" in name:
        return [term["args"][0], *flatten_list(term["args"][1], sort_marker)]
    raise AssertionError(f"unexpected {sort_marker} list node: {name}")


def extract_nullary_rule_rhs(rule_name: str) -> str:
    lines = VERIFICATION.read_text(encoding="utf-8").splitlines()
    marker = f"  rule {rule_name}"
    start = next(i for i, line in enumerate(lines) if line == marker)
    rhs_lines: list[str] = []
    for line in lines[start + 1 :]:
        if not line.strip():
            break
        rhs_lines.append(line)
    assert rhs_lines and rhs_lines[0].lstrip().startswith("=>")
    rhs_lines[0] = rhs_lines[0].replace("=>", "", 1)
    return "\n".join(rhs_lines).strip()


def replace_nullary(term: dict, replacements: dict[str, dict]) -> dict:
    name = label(term)
    for prefix, replacement in replacements.items():
        if name.startswith(prefix) and not term.get("args"):
            return replacement
    if term.get("node") == "KApply":
        return {
            **term,
            "args": [replace_nullary(arg, replacements) for arg in term["args"]],
        }
    return term


def digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


module = run_kast_file(WORK / "solution.regenerated.mpy")
assert label(module).startswith("Module(_)_")
module_statements = flatten_list(module["args"][0], "Stmts")
functions = [
    term for term in module_statements if label(term).startswith("FuncDef(_,_,_)_")
]
assert len(functions) == 1
actual_function = functions[0]
actual_name, params_wrapper, actual_body = actual_function["args"]
assert actual_name["token"] == '"parse_nested_parens"'
assert label(params_wrapper).startswith("Params(_)_")
actual_params = params_wrapper["args"][0]
assert [token["token"] for token in flatten_list(actual_params, "ParamNames")] == [
    '"paren_string"'
]

actual_body_statements = flatten_list(actual_body, "Stmts")
actual_for = [
    term for term in actual_body_statements if label(term).startswith("For(_,_,_)_")
]
assert len(actual_for) == 1
actual_loop_body = actual_for[0]["args"][2]

proof_loop_body = run_kast_expression(
    extract_nullary_rule_rhs("parseLoopBody"), "Stmts"
)
assert proof_loop_body == actual_loop_body

proof_function_body_unexpanded = run_kast_expression(
    extract_nullary_rule_rhs("parseFunctionBody"), "Stmts"
)
proof_function_body = replace_nullary(
    proof_function_body_unexpanded,
    {"parseLoopBody_VERIFICATION_Stmts": proof_loop_body},
)
assert proof_function_body == actual_body

proof_closure_unexpanded = run_kast_expression(
    extract_nullary_rule_rhs("parseNestedParensClosure"), "Val"
)
proof_closure = replace_nullary(
    proof_closure_unexpanded,
    {
        "parseFunctionBody_VERIFICATION_Stmts": proof_function_body,
        "parseLoopBody_VERIFICATION_Stmts": proof_loop_body,
    },
)
assert label(proof_closure).startswith("closureVal(_,_,_)_")
closure_params, closure_body, closure_def_env = proof_closure["args"]
assert closure_params == actual_params
assert closure_body == actual_body
assert closure_def_env.get("token") == "0"

print(f"module_statements={len(module_statements)}")
print("target_function_name=parse_nested_parens")
print("target_parameter=paren_string")
print(f"actual_loop_body_sha256={digest(actual_loop_body)}")
print(f"proof_loop_body_sha256={digest(proof_loop_body)}")
print(f"actual_function_body_sha256={digest(actual_body)}")
print(f"proof_function_body_sha256={digest(proof_function_body)}")
print("closure_definition_environment=0")
print("LOOP_CONSTRUCTOR_IDENTITY=PASS")
print("FUNCTION_CONSTRUCTOR_IDENTITY=PASS")
print("CLOSURE_BINDING_BODY_IDENTITY=PASS")
