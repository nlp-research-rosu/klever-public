#!/usr/bin/env python3
"""Mechanical program-term comparison and concrete claim witnesses."""

from __future__ import annotations

import importlib.util
import re


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


def balanced_application(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced Module application")


def tokens(text: str) -> list[str]:
    token_pattern = re.compile(
        r'"(?:\\.|[^"\\])*"'
        r"|[A-Za-z_#][A-Za-z0-9_#-]*"
        r"|\.[A-Za-z][A-Za-z0-9]*"
        r"|-?(?:[0-9]+\.[0-9]+|[0-9]+)"
        r"|[(),]"
    )
    return token_pattern.findall(text)


def row_acc(found, left, threshold, i, j, values):
    for right in values:
        if i < j:
            found = found or abs(left - right) < threshold
        j += 1
    return found


def outer_acc(found, values, threshold, i, remaining):
    for left in remaining:
        found = row_acc(found, left, threshold, i, 0, values)
        i += 1
    return found


solution_mpy = open("/tmp/audit-work/reconstruction/solution.mpy", encoding="utf-8").read()
spec_k = open("/tmp/audit-work/reconstruction/spec.k", encoding="utf-8").read()
solution_start = solution_mpy.index("Module(")
claim_start = spec_k.index("Module(", spec_k.index("#loadAll("))
solution_module = balanced_application(solution_mpy, solution_start)
claim_module = balanced_application(spec_k, claim_start)
solution_tokens = tokens(solution_module)
claim_tokens = [token for token in tokens(claim_module) if token != ".Stmts"]

print("COMMAND: python3 /audit-output/evidence/04_pinning_and_witnesses.py")
print("SOLUTION_MODULE_TOKEN_COUNT:", len(solution_tokens))
print("CLAIM_MODULE_TOKEN_COUNT_AFTER_EMPTY_STMTS_NORMALIZATION:", len(claim_tokens))
print("MODULE_CONSTRUCTOR_TOKENS_IDENTICAL:", solution_tokens == claim_tokens)
if solution_tokens != claim_tokens:
    for index, (left, right) in enumerate(zip(solution_tokens, claim_tokens)):
        if left != right:
            print("FIRST_TOKEN_DIFFERENCE:", index, repr(left), repr(right))
            break

canonical = load_function("trusted_canonical_ground", "/reference/canonical.py")
generated = load_function("submitted_generated_ground", "/candidate/solution.py")
ground_cases = [
    ([], 0.5),
    ([1.0], 1.0),
    ([1.0, 2.0, 3.0], 0.5),
    ([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3),
    ([0.0, 0.1], 0.2),
]
ground_mismatches = 0
for values, threshold in ground_cases:
    formal_summary = outer_acc(False, values, threshold, 0, values)
    canonical_result = canonical(list(values), threshold)
    generated_result = generated(list(values), threshold)
    agrees = formal_summary is canonical_result is generated_result
    ground_mismatches += not agrees
    print(
        "GROUND",
        repr(values),
        repr(threshold),
        "outerAcc=" + repr(formal_summary),
        "canonical=" + repr(canonical_result),
        "generated=" + repr(generated_result),
        "agree=" + repr(agrees),
    )

print(
    "ENTRY_SATISFYING_STATE:",
    "VS=vCons(0.0,vCons(0.1,.ValSeq)); T=0.2; allFloats(VS)=true",
)
print(
    "OUTER_SATISFYING_STATE:",
    "VS=REM=vCons(0.0,vCons(0.1,.ValSeq)); T=0.2; I=0; "
    "B=false; allFloats(VS)=allFloats(REM)=true; 0<=I",
)
print(
    "INNER_SATISFYING_STATE:",
    "VS=REM=vCons(0.0,vCons(0.1,.ValSeq)); A=0.0; T=0.2; "
    "I=0; J=0; B=false; isFloat(A)=true; 0<=I; 0<=J",
)

failure = solution_tokens != claim_tokens or ground_mismatches != 0
print("SCRIPT_EXIT=" + ("1" if failure else "0"))
raise SystemExit(1 if failure else 0)
