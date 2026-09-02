#!/usr/bin/env python3
"""Mechanical constructor-level comparison for the submitted MPY program and claims."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/95-check-dict-case")


def balanced_term(text: str, needle: str, start: int = 0) -> str:
    begin = text.index(needle, start)
    open_index = text.index("(", begin)
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
                return text[begin : index + 1]
    raise ValueError(f"unbalanced term beginning {needle!r}")


def term_args(term: str) -> list[str]:
    open_index = term.index("(")
    inner = term[open_index + 1 : -1]
    parts: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(inner):
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
            parts.append(inner[start:index])
            start = index + 1
    parts.append(inner[start:])
    return parts


def normalize(text: str) -> str:
    normalized = re.sub(r"\s+", "", text)
    # The trusted translator prints an empty List{Expr} as blank concrete-list
    # syntax, while claims spell the same unit explicitly as .Exprs.
    normalized = normalized.replace(",.Exprs)", ",)")
    return normalized


def extract_rule_rhs(text: str, rule_name: str, next_marker: str) -> str:
    match = re.search(rf"rule\s+{re.escape(rule_name)}\(\)\s*=>", text)
    if not match:
        raise ValueError(rule_name)
    end = text.index(next_marker, match.end())
    return text[match.end() : end]


solution_text = (ROOT / "regenerated-solution.mpy").read_text()
spec_text = (ROOT / "spec.k").read_text()
verification_text = (ROOT / "verification.k").read_text()

translated_func = balanced_term(solution_text, "FuncDef(")
claim_func = balanced_term(spec_text, "FuncDef(")
translated_args = term_args(translated_func)
claim_args = term_args(claim_func)
translated_body = translated_args[2]
claim_body = claim_args[2]

closure = balanced_term(spec_text, "closureVal(")
closure_args = term_args(closure)
closure_body = closure_args[1]

loop = balanced_term(translated_body, "For(")
loop_body = term_args(loop)[2]
return_term = balanced_term(translated_body, "Return(", translated_body.rfind("Return("))
return_expr = term_args(return_term)[0]

alias_loop = extract_rule_rhs(verification_text, "checkDictLoopBody", "syntax Expr")
alias_return = extract_rule_rhs(verification_text, "checkDictReturn", "syntax Stmts")
alias_body = extract_rule_rhs(verification_text, "checkDictBody", "// isStringKey")
expanded_alias_body = (
    alias_body.replace("checkDictLoopBody()", alias_loop)
    .replace("checkDictReturn()", alias_return)
)

comparisons = [
    ("translated FuncDef equals target claim FuncDef", translated_func, claim_func),
    ("translated function body equals target body", translated_body, claim_body),
    ("translated function body equals postcondition closure body", translated_body, closure_body),
    (
        "translated function body equals recursively expanded checkDictBody",
        translated_body,
        expanded_alias_body,
    ),
    ("translated loop body equals checkDictLoopBody expansion", loop_body, alias_loop),
    ("translated return expression equals checkDictReturn expansion", return_expr, alias_return),
]

print("MECHANICAL PROGRAM-PINNING CHECK")
failures = 0
for label, left, right in comparisons:
    left_normal = normalize(left)
    right_normal = normalize(right)
    same = left_normal == right_normal
    failures += not same
    print(
        f"{'PASS' if same else 'FAIL'} | {label} | "
        f"left_sha256={hashlib.sha256(left_normal.encode()).hexdigest()} "
        f"right_sha256={hashlib.sha256(right_normal.encode()).hexdigest()}"
    )
    if not same:
        print("LEFT_NORMALIZED", left_normal)
        print("RIGHT_NORMALIZED", right_normal)
print(f"FAILURES: {failures}")
raise SystemExit(1 if failures else 0)
