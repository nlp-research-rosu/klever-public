#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and proof bodies."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path("/tmp/audit-work/37-sort-even")


def extract_call(text: str, name: str, start: int = 0) -> str:
    marker = name + "("
    begin = text.index(marker, start)
    depth = 0
    quoted = False
    escaped = False
    for pos in range(begin + len(name), len(text)):
        char = text[pos]
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
                return text[begin : pos + 1]
    raise ValueError(f"unbalanced {name} call")


def split_args(call: str) -> list[str]:
    inner = call[call.index("(") + 1 : -1]
    args: list[str] = []
    depth = 0
    quoted = False
    escaped = False
    last = 0
    for pos, char in enumerate(inner):
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
            args.append(inner[last:pos])
            last = pos + 1
    args.append(inner[last:])
    return args


def normalize(term: str) -> str:
    term = re.sub(r"//[^\n]*", "", term)
    term = re.sub(r"\s+", "", term)
    term = term.replace("ListExpr(.Exprs)", "ListExpr()")
    return term


def rhs_between(text: str, rule_name: str, next_marker: str) -> str:
    match = re.search(rf"(?m)^\s*rule\s+{re.escape(rule_name)}\s*=>", text)
    if match is None:
        raise ValueError(f"rule {rule_name} not found")
    end = text.index(next_marker, match.end())
    return text[match.end() : end]


def main() -> int:
    mpy = (ROOT / "solution.mpy").read_text()
    verification = (ROOT / "verification.k").read_text()
    spec = (ROOT / "spec.k").read_text()

    func = extract_call(mpy, "FuncDef")
    func_args = split_args(func)
    if len(func_args) != 3:
        raise ValueError(f"expected three FuncDef arguments, got {len(func_args)}")
    source_name = normalize(func_args[0])
    source_params = normalize(func_args[1])
    source_body = normalize(func_args[2])

    loop_rhs = normalize(
        rhs_between(verification, "loopBody", '\n  syntax Stmts ::= "sortEvenBody"')
    )
    proof_body = normalize(
        rhs_between(verification, "sortEvenBody", '\n  syntax Val ::= "sortEvenClosure"')
    )
    proof_body_expanded = proof_body.replace("loopBody", loop_rhs)

    source_for = extract_call(source_body, "For")
    source_for_args = split_args(source_for)
    source_loop_body = normalize(source_for_args[2])

    checks = {
        "function_name_is_sort_even": source_name == '"sort_even"',
        "parameter_constructor_is_l": source_params == 'Params("l")',
        "loop_body_constructor_equal": source_loop_body == loop_rhs,
        "expanded_function_body_constructor_equal": source_body == proof_body_expanded,
        "closure_rule_exact": bool(
            re.search(
                r'rule\s+sortEvenClosure\s*=>\s*closureVal\(\s*\("l"\)\s*,\s*sortEvenBody\s*,\s*0\s*\)',
                verification,
                re.S,
            )
        ),
        "entry_scope_binds_sort_even_closure": bool(
            re.search(r'"sort_even"\s*\|->\s*sortEvenClosure', spec)
        ),
        "entry_k_calls_sort_even_on_symbolic_list": bool(
            re.search(
                r'Call\(\s*Name\("sort_even"\)\s*,\s*list\(VS\)\s*\)\s*~>\s*#observeResult',
                spec,
                re.S,
            )
        ),
        "entry_result_is_constrained_summary": bool(
            re.search(
                r'=>\s*list\(\s*assembledEvenSort\(\s*sortVS\(evenIndices\(VS\)\)\s*,\s*oddIndices\(VS\)\s*\)\s*\)',
                spec,
                re.S,
            )
        ),
    }
    for name, result in checks.items():
        print(f"{name}={result}")
    print(f"source_body_normalized={source_body}")
    print(f"proof_body_expanded_normalized={proof_body_expanded}")
    print(f"source_loop_body_normalized={source_loop_body}")
    print(f"proof_loop_body_normalized={loop_rhs}")
    print(f"CHECK_COUNT={len(checks)}")
    print(f"FAILURE_COUNT={sum(not result for result in checks.values())}")
    return 1 if any(not result for result in checks.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
