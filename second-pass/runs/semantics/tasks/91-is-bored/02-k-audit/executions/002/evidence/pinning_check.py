#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and claim bodies."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
DEFINITION = ROOT / "verification-kompiled"


def kast_expression(expression: str, sort: str) -> dict:
    command = [
        "kast",
        "--expression",
        expression,
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--sort",
        sort,
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True
    )
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        raise RuntimeError(
            f"kast expression failed with status {completed.returncode}"
        )
    return json.loads(completed.stdout)["term"]


def kast_file(path: Path, sort: str, module: str) -> dict:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        module,
        "--sort",
        sort,
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True
    )
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        raise RuntimeError(f"kast file failed with status {completed.returncode}")
    return json.loads(completed.stdout)["term"]


def rule_rhs(source: str, rule_name: str, next_marker: str) -> str:
    pattern = (
        rf"(?ms)^  rule {re.escape(rule_name)}\s*\n"
        rf"\s*=>\s*(.*?)\n{re.escape(next_marker)}"
    )
    match = re.search(pattern, source)
    if match is None:
        raise RuntimeError(f"cannot extract RHS for {rule_name}")
    return match.group(1)


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def find_first(term: dict, prefix: str) -> dict:
    if term.get("node") == "KApply" and label(term).startswith(prefix):
        return term
    for argument in term.get("args", []):
        found = find_first(argument, prefix)
        if found:
            return found
    return {}


def replace_constant(term: dict, prefix: str, replacement: dict) -> dict:
    if (
        term.get("node") == "KApply"
        and not term.get("args")
        and label(term).startswith(prefix)
    ):
        return replacement
    answer = dict(term)
    if "args" in term:
        answer["args"] = [
            replace_constant(argument, prefix, replacement)
            for argument in term["args"]
        ]
    return answer


verification_source = (ROOT / "verification.k").read_text()
loop_rhs = rule_rhs(
    verification_source, "boredLoopBody", "  rule boredFunctionBody"
)
function_rhs = rule_rhs(
    verification_source,
    "boredFunctionBody",
    "  // The three scanner states",
)
# The program parser represents empty statement-list arguments by an omitted
# list item; `.Stmts` is the equivalent K-definition notation.
loop_rhs = loop_rhs.replace(".Stmts", "")
function_rhs = function_rhs.replace(".Stmts", "")
loop_from_verification = kast_expression(loop_rhs, "Stmts")
function_from_verification = kast_expression(function_rhs, "Stmts")
expanded_function = replace_constant(
    function_from_verification,
    "boredLoopBody",
    loop_from_verification,
)

module_term = kast_file(ROOT / "solution.mpy", "Module", "MPY-SYNTAX")
function_definition = find_first(module_term, "FuncDef(")
if not function_definition:
    raise RuntimeError("translated is_bored function not found")
translated_body = function_definition["args"][2]
translated_for = find_first(translated_body, "For(")
if not translated_for:
    raise RuntimeError("translated for loop not found")
translated_loop = translated_for["args"][2]

print(f"function_name_token={function_definition['args'][0]['token']}")
print("parameter_term=" + json.dumps(function_definition["args"][1], sort_keys=True))
print(
    "loop_body_constructor_identity="
    + str(translated_loop == loop_from_verification)
)
print(
    "function_body_constructor_identity="
    + str(translated_body == expanded_function)
)
print(
    "claim_function_rhs_sha256="
    + __import__("hashlib").sha256(
        json.dumps(expanded_function, sort_keys=True).encode()
    ).hexdigest()
)
print(
    "translated_function_body_sha256="
    + __import__("hashlib").sha256(
        json.dumps(translated_body, sort_keys=True).encode()
    ).hexdigest()
)

assert translated_loop == loop_from_verification
assert translated_body == expanded_function
