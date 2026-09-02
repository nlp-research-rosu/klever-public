#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and entry claim."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def matching_paren(text: str, open_index: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced constructor term")


def top_level_commas(text: str) -> list[int]:
    commas = []
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            commas.append(index)
    return commas


def compact_body(text: str) -> str:
    # `.Stmts` is the identity of the submitted translator's statement-list sort.
    return re.sub(r"\s+", "", text).replace(".Stmts", "")


solution = Path("/tmp/audit-work/proof/regenerated-solution.mpy").read_text()
spec = Path("/tmp/audit-work/proof/spec.k").read_text()

function_marker = 'FuncDef("correct_bracketing", Params("brackets"),'
function_start = solution.index(function_marker)
function_open = solution.index("(", function_start)
function_close = matching_paren(solution, function_open)
function_inner = solution[function_open + 1 : function_close]
function_commas = top_level_commas(function_inner)
if len(function_commas) != 2:
    raise AssertionError(f"unexpected FuncDef arguments: {function_commas}")
translated_body = function_inner[function_commas[1] + 1 :]

binding_start = spec.index('"correct_bracketing" |->')
closure_start = spec.index("closureVal(", binding_start)
closure_open = spec.index("(", closure_start)
closure_close = matching_paren(spec, closure_open)
closure_inner = spec[closure_open + 1 : closure_close]
closure_commas = top_level_commas(closure_inner)
if len(closure_commas) != 2:
    raise AssertionError(f"unexpected closureVal arguments: {closure_commas}")
claim_params = closure_inner[: closure_commas[0]]
claim_body = closure_inner[closure_commas[0] + 1 : closure_commas[1]]
claim_environment = closure_inner[closure_commas[1] + 1 :]

translated_normal = compact_body(translated_body)
claim_normal = compact_body(claim_body)
parameters_match = compact_body(claim_params) == '("brackets",.ParamNames)'
environment_match = compact_body(claim_environment) == "0"
body_match = translated_normal == claim_normal

print(f"function_marker_count={solution.count(function_marker)}")
print(f"entry_binding_count={spec.count(chr(34) + 'correct_bracketing' + chr(34) + ' |->')}")
print("allowed_normalizations=whitespace,.Stmts-list-identity,Params-to-ParamNames")
print(f"parameters_match={parameters_match}")
print(f"definition_environment_match={environment_match}")
print(f"body_match={body_match}")
print(f"translated_body_sha256={hashlib.sha256(translated_normal.encode()).hexdigest()}")
print(f"claim_body_sha256={hashlib.sha256(claim_normal.encode()).hexdigest()}")

if not (
    solution.count(function_marker) == 1
    and parameters_match
    and environment_match
    and body_match
):
    print("TRANSLATED_NORMAL:")
    print(translated_normal)
    print("CLAIM_NORMAL:")
    print(claim_normal)
    sys.exit(1)
