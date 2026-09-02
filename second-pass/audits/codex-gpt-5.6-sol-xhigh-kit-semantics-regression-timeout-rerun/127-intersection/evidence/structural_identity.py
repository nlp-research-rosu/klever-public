#!/usr/bin/env python3
"""Reviewer-authored structural pinning checks."""

import ast
import json
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/scratch")
EVIDENCE = Path("/audit-output/evidence")


def parse_k_json(*arguments):
    process = subprocess.run(
        ["kast", *arguments, "--output", "json"],
        check=True,
        text=True,
        capture_output=True,
        cwd=SCRATCH,
    )
    return json.loads(process.stdout)["term"]


def only_function(path):
    module = ast.parse(path.read_text(encoding="utf-8"))
    functions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1:
        raise RuntimeError(f"expected one function in {path}, found {len(functions)}")
    return ast.dump(functions[0], include_attributes=False)


def main():
    translated_module = parse_k_json(
        "solution.mpy",
        "--definition",
        "verification-kompiled",
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
    )
    statements = translated_module["args"][0]
    translated_function = statements["args"][0]
    translated_tail = statements["args"][1]
    if not translated_function["label"]["name"].startswith("FuncDef("):
        raise RuntimeError("solution.mpy does not begin with FuncDef")
    if translated_tail.get("arity") != 0:
        raise RuntimeError("solution.mpy has unexpected trailing statements")

    function_name, params_wrapper, translated_body = translated_function["args"]
    if function_name["token"] != '"intersection"':
        raise RuntimeError("translated entry point is not intersection")
    translated_params = params_wrapper["args"][0]

    verification_text = (SCRATCH / "verification.k").read_text(encoding="utf-8")
    match = re.search(
        r"(?ms)^  rule intersectionClosure =>.*?(?=^  rule scanPrime)",
        verification_text,
    )
    if match is None:
        raise RuntimeError("could not isolate intersectionClosure rule")
    rule_text = match.group(0).strip().removeprefix("rule ")
    parsed_rule = parse_k_json(
        "--expression",
        rule_text,
        "--input",
        "rule",
        "--definition",
        "verification-kompiled",
        "--module",
        "VERIFICATION",
    )
    proof_params, proof_body, proof_scope = parsed_rule["rhs"]["args"]

    if translated_params != proof_params:
        raise RuntimeError("proof closure parameters differ from solution.mpy")
    if translated_body != proof_body:
        raise RuntimeError("proof closure body differs from solution.mpy")
    if proof_scope.get("token") != "0":
        raise RuntimeError("proof closure does not capture module scope 0")

    if only_function(SCRATCH / "solution.py") != only_function(
        EVIDENCE / "concrete_harness.py"
    ):
        raise RuntimeError("concrete harness function differs from solution.py")

    print(
        "PROGRAM_PINNING=PASS "
        "entry=intersection "
        "translated_params_equal=true "
        "translated_body_equal=true "
        "closure_scope=0 "
        "harness_python_ast_equal=true"
    )


if __name__ == "__main__":
    main()
