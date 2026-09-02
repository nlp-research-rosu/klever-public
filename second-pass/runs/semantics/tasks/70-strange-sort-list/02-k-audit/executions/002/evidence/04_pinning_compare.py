#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and claim macros."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/task70")
parser = argparse.ArgumentParser()
parser.add_argument("--mpy", type=Path, default=ROOT / "solution.mpy")
parser.add_argument("--verification", type=Path, default=ROOT / "verification.k")
parser.add_argument("--spec", type=Path, default=ROOT / "spec.k")
args = parser.parse_args()

mpy = args.mpy.read_text(encoding="utf-8")
verification = args.verification.read_text(encoding="utf-8")
spec = args.spec.read_text(encoding="utf-8")


def find_balanced_call(text: str, start: int) -> str:
    open_paren = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
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
    raise ValueError("unbalanced constructor")


def split_top_level(inner: str) -> list[str]:
    parts: list[str] = []
    begin = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(inner):
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
        elif char == "," and depth == 0:
            parts.append(inner[begin:index])
            begin = index + 1
    parts.append(inner[begin:])
    return parts


def call_args(call: str) -> list[str]:
    return split_top_level(call[call.index("(") + 1 : -1])


def rule_rhs_until(rule_name: str, end_marker: str) -> str:
    start = verification.index(f"rule {rule_name}()")
    rhs = verification.index("=>", start) + 2
    end = verification.index(end_marker, rhs)
    return verification[rhs:end].strip()


def normalize(term: str) -> str:
    term = re.sub(r"(?m)^\s*//[^\n]*(?:\n|$)", "", term)
    term = re.sub(r"\s+", "", term)
    term = term.replace("ListExpr(.Exprs)", "ListExpr()")
    return term


func_start = mpy.index('FuncDef("strange_sort_list"')
func_call = find_balanced_call(mpy, func_start)
func_args = call_args(func_call)
if len(func_args) != 3:
    raise AssertionError(f"expected three FuncDef arguments, got {len(func_args)}")
if normalize(func_args[0]) != '"strange_sort_list"':
    raise AssertionError(f"wrong function binding: {func_args[0]!r}")
if normalize(func_args[1]) != 'Params("lst")':
    raise AssertionError(f"wrong function parameters: {func_args[1]!r}")
translated_body = normalize(func_args[2])

condition = normalize(
    rule_rhs_until("strangeCondition", "\n\n  syntax Stmts ::= strangeLoopBody")
)
loop_body = normalize(
    rule_rhs_until("strangeLoopBody", "\n\n  syntax Stmts ::= strangeBody")
)
macro_body = normalize(rule_rhs_until("strangeBody", "\n\n  // Element selected"))
expanded_body = macro_body.replace("strangeCondition()", condition).replace(
    "strangeLoopBody()", loop_body
)

print(f"translated-body-sha256={hashlib.sha256(translated_body.encode()).hexdigest()}")
print(f"expanded-macro-sha256={hashlib.sha256(expanded_body.encode()).hexdigest()}")
print(f"translated-body={translated_body}")
print(f"expanded-macro={expanded_body}")
if translated_body != expanded_body:
    raise AssertionError("translated function body and expanded strangeBody macro differ")

call_pattern = re.compile(
    r'Call\(\s*closureVal\(\s*\("lst"\s*,\s*\.ParamNames\)\s*,\s*'
    r"strangeBody\(\)\s*,\s*0\s*\)\s*,\s*list\(INPUT:ValSeq\)\s*\)",
    re.MULTILINE,
)
if not call_pattern.search(spec):
    raise AssertionError("entry claim does not call the pinned closure/body/argument")

print("PINNING_COMPARISON=PASS")
