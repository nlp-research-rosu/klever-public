#!/usr/bin/env python3
"""Mechanical constructor-level pinning check for solution.mpy versus spec.k."""

from __future__ import annotations

import hashlib
from pathlib import Path


def extract_balanced(text: str, marker: str, occurrence: int = 0) -> str:
    start = -1
    search_from = 0
    for _ in range(occurrence + 1):
        start = text.index(marker, search_from)
        search_from = start + len(marker)
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced term beginning {marker!r}")


def strip_layout(text: str) -> str:
    output: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    return "".join(output)


def normalize_empty_lists(text: str) -> str:
    # The translator emits empty K list productions by omission.  The spec uses
    # the equivalent explicit unit labels accepted by the same K list syntax.
    return (
        strip_layout(text)
        .replace("ListExpr()", "ListExpr(.Exprs)")
        .replace(",.Stmts)", ",)")
    )


def top_level_args(term: str) -> list[str]:
    first = term.index("(")
    last = len(term) - 1
    args: list[str] = []
    start = first + 1
    depth = 0
    quoted = False
    escaped = False
    for index in range(first + 1, last):
        char = term[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(term[start:index])
            start = index + 1
    args.append(term[start:last])
    return args


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    translated_text = Path("/tmp/audit-work/proof/solution.regenerated.mpy").read_text()
    spec_text = Path("/candidate/spec.k").read_text()

    translated_func = normalize_empty_lists(extract_balanced(translated_text, "FuncDef("))
    claimed_func = normalize_empty_lists(extract_balanced(spec_text, "FuncDef("))
    closure = normalize_empty_lists(extract_balanced(spec_text, "closureVal("))

    translated_args = top_level_args(translated_func)
    claimed_args = top_level_args(claimed_func)
    closure_args = top_level_args(closure)

    checks = {
        "translated_func_equals_claimed_func": translated_func == claimed_func,
        "function_name_equals": translated_args[0] == claimed_args[0] == '"get_positive"',
        "function_params_equals": translated_args[1] == claimed_args[1] == 'Params("l")',
        "func_body_equals_installed_closure_body": claimed_args[2] == closure_args[1],
        "closure_param_equals": closure_args[0] == '"l"',
        "closure_definition_scope_is_module_zero": closure_args[2] == "0",
        "entry_calls_installed_name_with_symbolic_list": (
            '~>Call(Name("get_positive"),list(VS:ValSeq))=>ref(0)'
            in strip_layout(spec_text)
        ),
    }
    print(f"TRANSLATED_FUNC_SHA256={digest(translated_func)}")
    print(f"CLAIMED_FUNC_SHA256={digest(claimed_func)}")
    print(f"CLOSURE_BODY_SHA256={digest(closure_args[1])}")
    for name, result in checks.items():
        print(f"{name}={result}")
    print(f"ALL_CHECKS={all(checks.values())}")
    return int(not all(checks.values()))


if __name__ == "__main__":
    raise SystemExit(main())
