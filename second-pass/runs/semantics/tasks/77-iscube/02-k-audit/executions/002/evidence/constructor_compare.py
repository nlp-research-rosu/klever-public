#!/usr/bin/env python3
"""Mechanical constructor comparison between solution.mpy and iscubeClosure."""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_SOLUTION = Path("/tmp/audit-work/candidate/solution.mpy")
DEFAULT_VERIFICATION = Path("/tmp/audit-work/candidate/verification.k")


def strip_line_comments(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def find_call(text: str, name: str, start: int = 0) -> str:
    marker = name + "("
    index = text.index(marker, start)
    open_index = index + len(name)
    depth = 0
    quoted = False
    escaped = False
    for cursor in range(open_index, len(text)):
        char = text[cursor]
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
                return text[index : cursor + 1]
    raise ValueError(f"unclosed call {name}")


def split_call(call: str) -> tuple[str, list[str]]:
    name, remainder = call.split("(", 1)
    interior = remainder[:-1]
    arguments = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(interior):
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
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            arguments.append(interior[start:index])
            start = index + 1
    arguments.append(interior[start:])
    return name.strip(), arguments


def normalize(text: str) -> str:
    output = []
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", type=Path, default=DEFAULT_SOLUTION)
    parser.add_argument("--verification", type=Path, default=DEFAULT_VERIFICATION)
    args = parser.parse_args()
    solution_text = strip_line_comments(args.solution.read_text())
    verification_text = strip_line_comments(args.verification.read_text())

    _, module_args = split_call(find_call(solution_text, "Module"))
    if len(module_args) != 1:
        raise AssertionError(f"expected one top-level source statement: {module_args}")
    _, function_args = split_call(find_call(module_args[0], "FuncDef"))
    if len(function_args) != 3:
        raise AssertionError(f"unexpected FuncDef arity: {len(function_args)}")
    source_name, source_params, source_body = map(normalize, function_args)

    rule_index = verification_text.index("rule iscubeClosure =>")
    _, closure_args = split_call(
        find_call(verification_text, "closureVal", rule_index)
    )
    if len(closure_args) != 3:
        raise AssertionError(f"unexpected closureVal arity: {len(closure_args)}")
    closure_params, closure_body, closure_defining_scope = map(normalize, closure_args)

    source_param_names = source_params
    expected_source_params = 'Params("a")'
    expected_closure_params = '("a",.ParamNames)'
    source_body_normalized = source_body.removesuffix(".Stmts")
    closure_body_normalized = closure_body.removesuffix(".Stmts")

    checks = {
        "source_name_is_iscube": source_name == '"iscube"',
        "source_params_are_single_a": source_param_names == expected_source_params,
        "closure_params_are_single_a": closure_params == expected_closure_params,
        "constructor_body_equal_ignoring_explicit_empty_terminator": (
            source_body_normalized == closure_body_normalized
        ),
        "closure_defining_scope_is_module_zero": closure_defining_scope == "0",
    }

    print(f"solution={args.solution}")
    print(f"verification={args.verification}")
    print(f"source_name={source_name}")
    print(f"source_params={source_params}")
    print(f"closure_params={closure_params}")
    print(f"closure_defining_scope={closure_defining_scope}")
    print(f"source_body_normalized={source_body_normalized}")
    print(f"closure_body_normalized={closure_body_normalized}")
    for name, result in checks.items():
        print(f"check[{name}]={result}")
    print(f"ALL_CHECKS_PASS={all(checks.values())}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
