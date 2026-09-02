#!/usr/bin/env python3
"""Mechanical constructor-body comparison and entry-configuration inspection."""

from __future__ import annotations

import re
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/candidate/solution.mpy")
VERIFICATION = Path("/tmp/audit-work/candidate/verification.k")
SPEC = Path("/tmp/audit-work/candidate/spec.k")


def strip_space(text: str) -> str:
    return re.sub(r"\s+", "", text)


def balanced_call(text: str, marker: str) -> str:
    start = text.index(marker)
    open_index = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
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
    raise ValueError(f"unbalanced call beginning {marker!r}")


def rule_rhs_between(text: str, marker: str, end_marker: str) -> str:
    start = text.index(marker) + len(marker)
    end = text.index(end_marker, start)
    return text[start:end].strip()


def main() -> int:
    solution = SOLUTION.read_text()
    verification = VERIFICATION.read_text()
    spec = SPEC.read_text()

    find_zero_call = balanced_call(solution, 'FuncDef("find_zero"')
    body_marker = 'FuncDef("find_zero", Params("xs"),'
    assert find_zero_call.startswith(body_marker)
    submitted_body = find_zero_call[len(body_marker) : -1].strip()

    bracket_body = rule_rhs_between(
        verification, "rule bracketLoop =>", "syntax Stmt ::= \"bisectLoop\""
    )
    bisect_body = rule_rhs_between(
        verification, "rule bisectLoop =>", "syntax Stmts ::= \"findZeroBody\""
    )
    claimed_body = rule_rhs_between(
        verification, "rule findZeroBody =>", "syntax Module ::= \"solutionModule\""
    )
    expanded_claimed_body = re.sub(
        r"\bbracketLoop\b", lambda _: bracket_body, claimed_body
    )
    expanded_claimed_body = re.sub(
        r"\bbisectLoop\b", lambda _: bisect_body, expanded_claimed_body
    )
    bodies_equal = strip_space(submitted_body) == strip_space(expanded_claimed_body)

    poly_call = balanced_call(solution, 'FuncDef("poly"')
    poly_mentioned_in_find_zero = 'Name("poly")' in submitted_body
    direct_closure = 'closureVal(("xs", .ParamNames), findZeroBody, 0)' in spec
    module_loaded = "#loadAll(solutionModule)" in spec or "solutionModule" in spec
    module_scope_empty = "0 |-> scope(.Map, parent(-1))" in spec
    poly_binding_in_spec = bool(
        re.search(r'0\s*\|->\s*scope\([^)]*"poly"\s*\|->', spec, re.DOTALL)
    )
    calls_bound_find_zero = 'Call(Name("find_zero")' in spec

    print(f"submitted find_zero constructor bytes: {len(submitted_body)}")
    print(f"expanded claimed body constructor bytes: {len(expanded_claimed_body)}")
    print(f"whitespace-insensitive constructor body identity: {bodies_equal}")
    print(f"submitted poly definition found: {bool(poly_call)}")
    print(f"find_zero body contains Name(\"poly\"): {poly_mentioned_in_find_zero}")
    print(f"spec constructs closureVal directly: {direct_closure}")
    print(f"spec loads solutionModule: {module_loaded}")
    print(f"spec calls scope-bound Name(\"find_zero\"): {calls_bound_find_zero}")
    print(f"spec starts with empty module scope 0: {module_scope_empty}")
    print(f"spec supplies a poly binding in scope 0: {poly_binding_in_spec}")
    print(
        "binding conclusion: "
        + (
            "the body matches, but the claimed closure is not the submitted module binding "
            "and its required global poly binding is absent"
            if bodies_equal
            and direct_closure
            and module_scope_empty
            and not poly_binding_in_spec
            else "unexpected configuration; inspect manually"
        )
    )
    return 0 if bodies_equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
