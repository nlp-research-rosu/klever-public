#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and verification.k."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def matching_paren(text: str, open_index: int) -> int:
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
                return index
    raise ValueError("unmatched parenthesis")


def split_top_level(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(text):
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
            parts.append(text[start:index])
            start = index + 1
    parts.append(text[start:])
    return parts


def normalize(text: str) -> str:
    text = text.replace(".Stmts", "")
    output: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    return "".join(output)


def rhs_between(text: str, marker: str, next_marker: str) -> str:
    start = text.index(marker) + len(marker)
    end = text.index(next_marker, start)
    return text[start:end]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mpy", type=Path, required=True)
    parser.add_argument("--verification", type=Path, required=True)
    args = parser.parse_args()

    mpy = args.mpy.read_text()
    verification = args.verification.read_text()

    func_start = mpy.index('FuncDef("even_odd_palindrome"')
    open_index = mpy.index("(", func_start)
    close_index = matching_paren(mpy, open_index)
    func_arguments = split_top_level(mpy[open_index + 1 : close_index])
    if len(func_arguments) != 3:
        raise ValueError(f"expected 3 FuncDef arguments, got {len(func_arguments)}")
    mpy_name, mpy_params, mpy_body = func_arguments

    verification_body = rhs_between(
        verification, "rule solutionBody =>", 'syntax Module ::= "solutionModule"'
    )
    verification_module = rhs_between(
        verification, "rule solutionModule =>", "// Start from the standard"
    )

    expected_module = (
        'Module(FuncDef("even_odd_palindrome", Params("n"), solutionBody))'
    )
    body_same = normalize(mpy_body) == normalize(verification_body)
    module_same = normalize(verification_module) == normalize(expected_module)
    name_same = normalize(mpy_name) == '"even_odd_palindrome"'
    params_same = normalize(mpy_params) == 'Params("n")'

    print(f"function_name_identical={name_same}")
    print(f"parameters_identical={params_same}")
    print(f"constructor_body_identical={body_same}")
    print(f"solution_module_binding_identical={module_same}")
    print(f"normalized_mpy_body_sha256={hashlib.sha256(normalize(mpy_body).encode()).hexdigest()}")
    print(
        "normalized_verification_body_sha256="
        f"{hashlib.sha256(normalize(verification_body).encode()).hexdigest()}"
    )
    if not body_same:
        print(f"normalized_mpy_body={normalize(mpy_body)}")
        print(f"normalized_verification_body={normalize(verification_body)}")
    return 0 if all((name_same, params_same, body_same, module_same)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
