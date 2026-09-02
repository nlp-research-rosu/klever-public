#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and runCompare."""

from __future__ import annotations

import re
from pathlib import Path


def balanced_call(text: str, marker: str) -> str:
    start = text.index(marker)
    open_index = text.index("(", start)
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
                return text[start : index + 1]
    raise ValueError(f"unbalanced call after {marker}")


def split_top_level_arguments(call: str) -> list[str]:
    body = call[call.index("(") + 1 : -1]
    arguments: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(body):
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
            arguments.append(body[start:index])
            start = index + 1
    arguments.append(body[start:])
    return arguments


def normalize_statements(text: str) -> str:
    normalized = re.sub(r"\s+", "", text)
    # The translator's optional empty else branch parses as .Stmts.  The
    # verification file spells that identity explicitly.
    normalized = normalized.replace(",.Stmts)", ",)")
    return normalized


def main() -> None:
    solution = Path("/tmp/audit-work/137-compare-one/solution.mpy").read_text()
    verification = Path(
        "/tmp/audit-work/137-compare-one/verification.k"
    ).read_text()

    function_call = balanced_call(solution, 'FuncDef("compare_one"')
    function_args = split_top_level_arguments(function_call)
    if len(function_args) != 3:
        raise AssertionError(f"unexpected FuncDef arity: {len(function_args)}")
    if normalize_statements(function_args[1]) != 'Params("a","b")':
        raise AssertionError("submitted parameter list is not (a,b)")

    closure_call = balanced_call(verification, "closureVal(")
    closure_args = split_top_level_arguments(closure_call)
    if len(closure_args) != 3:
        raise AssertionError(f"unexpected closureVal arity: {len(closure_args)}")
    if normalize_statements(closure_args[0]) != '("a","b",.ParamNames)':
        raise AssertionError("runCompare closure parameter list is not (a,b)")
    if normalize_statements(closure_args[2]) != "0":
        raise AssertionError("runCompare parent scope is not scope 0")

    submitted_body = normalize_statements(function_args[2])
    executed_body = normalize_statements(closure_args[1])
    print(f"SUBMITTED_BODY_CHARS: {len(submitted_body)}")
    print(f"EXECUTED_BODY_CHARS: {len(executed_body)}")
    print(f"CONSTRUCTOR_BODY_IDENTITY: {submitted_body == executed_body}")
    if submitted_body != executed_body:
        raise AssertionError("runCompare does not execute the submitted body")


if __name__ == "__main__":
    main()
