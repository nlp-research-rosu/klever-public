#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and runSimplify."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def balanced_application(text: str, marker: str) -> str:
    start = text.index(marker)
    open_index = text.index("(", start + len(marker))
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
    raise ValueError(f"unterminated application after {marker}")


def split_application(application: str) -> tuple[str, list[str]]:
    open_index = application.index("(")
    name = application[:open_index].strip()
    inner = application[open_index + 1 : -1]
    args: list[str] = []
    start = 0
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
        elif char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(inner[start:index].strip())
            start = index + 1
    args.append(inner[start:].strip())
    return name, args


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    solution_text = Path("/tmp/audit-work/regenerated-solution.mpy").read_text()
    verification_text = Path("/tmp/audit-work/candidate/verification.k").read_text()

    function_application = balanced_application(solution_text, "FuncDef")
    function_name, function_args = split_application(function_application)
    closure_application = balanced_application(verification_text, "closureVal")
    closure_name, closure_args = split_application(closure_application)
    if len(function_args) != 3:
        raise AssertionError(f"FuncDef arity changed: {len(function_args)}")
    if len(closure_args) != 3:
        raise AssertionError(f"closureVal arity changed: {len(closure_args)}")

    submitted_name = compact(function_args[0])
    submitted_params = compact(function_args[1])
    submitted_body = compact(function_args[2])
    embedded_params = compact(closure_args[0])
    embedded_body = compact(closure_args[1])
    embedded_scope = compact(closure_args[2])

    name_ok = submitted_name == '"simplify"'
    params_ok = submitted_params == 'Params("x","n")' and embedded_params == '("x","n")'
    body_ok = submitted_body == embedded_body
    scope_ok = embedded_scope == "0"
    wrapper_preserves_arguments = "(X,N,.Vals)" in compact(verification_text)
    wrapper_applies_closure = "#applyK(toCall(closureVal(" in compact(verification_text)

    print(f"solution_constructor={function_name}")
    print(f"embedded_constructor={closure_name}")
    print(f"function_name_ok={name_ok}")
    print(f"parameters_match={params_ok}")
    print(f"scope_binding_is_0={scope_ok}")
    print(f"wrapper_preserves_X_N_order={wrapper_preserves_arguments}")
    print(f"wrapper_applies_constructed_closure={wrapper_applies_closure}")
    print(f"submitted_body_sha256={digest(submitted_body)}")
    print(f"embedded_body_sha256={digest(embedded_body)}")
    print(f"constructor_body_byte_equal_after_whitespace_normalization={body_ok}")
    print(f"submitted_body={submitted_body}")
    print(f"embedded_body={embedded_body}")

    ok = all(
        (
            function_name == "FuncDef",
            closure_name == "closureVal",
            name_ok,
            params_ok,
            body_ok,
            scope_ok,
            wrapper_preserves_arguments,
            wrapper_applies_closure,
        )
    )
    print(f"PINNING_CHECK_PASS={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
