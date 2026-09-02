#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and SPEC entry."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def balanced_term(text: str, start: int) -> str:
    """Return the constructor call beginning at start, respecting K strings."""
    open_at = text.index("(", start)
    depth = 0
    quoted = False
    escaped = False
    for pos in range(start, len(text)):
        ch = text[pos]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if pos >= open_at and depth == 0:
                return text[start : pos + 1]
    raise ValueError(f"unbalanced term at {start}")


def normalize_constructor_lists(term: str) -> str:
    # Explicit `.Stmts` tails in hand-written K and implicit empty list tails in
    # translated concrete syntax parse to the same list constructors.
    term = term.replace(".Stmts", "")
    return re.sub(r"\s+", "", term)


solution_text = (ROOT / "solution.mpy").read_text(encoding="utf-8")
spec_text = (ROOT / "spec.k").read_text(encoding="utf-8")

solution_module = balanced_term(solution_text, solution_text.index("Module("))
load_start = spec_text.index("Module(", spec_text.index("#loadAll("))
claim_module = balanced_term(spec_text, load_start)

solution_norm = normalize_constructor_lists(solution_module)
claim_norm = normalize_constructor_lists(claim_module)

print(f"solution_normalized_bytes={len(solution_norm)}")
print(f"claim_normalized_bytes={len(claim_norm)}")
print(f"module_constructor_equal={solution_norm == claim_norm}")
if solution_norm != claim_norm:
    raise SystemExit("entry claim does not execute the submitted module")

expected_post = "=>str(removeVowelsFrom(TEXT,.IntSeq))"
compact_spec = normalize_constructor_lists(spec_text)
print(f"result_is_constrained={expected_post in compact_spec}")
if expected_post not in compact_spec:
    raise SystemExit("expected result-constraining postcondition not found")

# The loaded closure body is repeated in the observable module-scope update.
function_start = solution_norm.index("FuncDef(")
solution_function = balanced_term(solution_norm, function_start)
closure_body_start = compact_spec.index(
    'Assign(Name("result"),Str(""))',
    compact_spec.index("<-closureVal("),
)
closure_return_end = compact_spec.index(
    "Return(Name(\"result\"))", closure_body_start
) + len('Return(Name("result"))')
closure_body = compact_spec[closure_body_start:closure_return_end]
solution_body_start = solution_function.index('Assign(Name("result"),Str(""))')
solution_body_end = solution_function.index('Return(Name("result"))') + len(
    'Return(Name("result"))'
)
solution_body = solution_function[solution_body_start:solution_body_end]
print(f"observable_closure_body_equal={closure_body == solution_body}")
if closure_body != solution_body:
    raise SystemExit("observable closure binding does not preserve the function body")
