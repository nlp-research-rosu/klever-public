#!/usr/bin/env python3
"""Compare the submitted FuncDef body with the closure body embedded in spec.k."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|=>|~>|\.?[A-Za-z#$][A-Za-z0-9_#$.-]*|-?\d+|[(),:]'
)


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def find_call(source: list[str], name: str, start: int = 0) -> tuple[int, int]:
    index = source.index(name, start)
    if source[index + 1] != "(":
        raise ValueError(f"{name} is not followed by '('")
    depth = 0
    for cursor in range(index + 1, len(source)):
        if source[cursor] == "(":
            depth += 1
        elif source[cursor] == ")":
            depth -= 1
            if depth == 0:
                return index, cursor
    raise ValueError(f"unclosed {name}")


def split_top_level_arguments(source: list[str], start: int, end: int) -> list[list[str]]:
    arguments: list[list[str]] = []
    current: list[str] = []
    depth = 0
    for token in source[start + 2 : end]:
        if token == "(":
            depth += 1
            current.append(token)
        elif token == ")":
            depth -= 1
            current.append(token)
        elif token == "," and depth == 0:
            arguments.append(current)
            current = []
        else:
            current.append(token)
    arguments.append(current)
    return arguments


def sha(source: list[str]) -> str:
    return hashlib.sha256("\x00".join(source).encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--program-root",
        type=Path,
        default=Path("/tmp/audit-work/133-sum-squares-audit"),
    )
    args = parser.parse_args()

    program_tokens = tokens((args.program_root / "solution.mpy").read_text())
    spec_tokens = tokens(
        Path("/tmp/audit-work/133-sum-squares-audit/spec.k").read_text()
    )

    func_start, func_end = find_call(program_tokens, "FuncDef")
    func_args = split_top_level_arguments(program_tokens, func_start, func_end)
    closure_start, closure_end = find_call(spec_tokens, "closureVal")
    closure_args = split_top_level_arguments(spec_tokens, closure_start, closure_end)

    if len(func_args) != 3 or len(closure_args) != 3:
        raise ValueError(
            f"unexpected arity FuncDef={len(func_args)} closureVal={len(closure_args)}"
        )
    program_body = func_args[2]
    embedded_body = closure_args[1]
    body_equal = program_body == embedded_body
    function_name = func_args[0] == ['"sum_squares"']
    program_params = func_args[1] == ["Params", "(", '"lst"', ")"]
    closure_params = closure_args[0] == ["(", '"lst"', ",", ".ParamNames", ")"]
    closure_env = closure_args[2] == ["0"]
    has_math_import = tokens('Import("math")') in [
        program_tokens[index : index + 4] for index in range(len(program_tokens) - 3)
    ]
    entry_executes_module = "Module" in spec_tokens
    entry_resolves_function_name = '"sum_squares"' in spec_tokens

    print(f"program_root={args.program_root}")
    print(f"function_name_sum_squares={function_name}")
    print(f"program_param_lst={program_params}")
    print(f"closure_param_lst={closure_params}")
    print(f"closure_defining_env_0={closure_env}")
    print(f"program_has_math_import={has_math_import}")
    print(f"program_body_sha256={sha(program_body)}")
    print(f"embedded_body_sha256={sha(embedded_body)}")
    print(f"body_token_identical={body_equal}")
    print(f"entry_k_executes_Module={entry_executes_module}")
    print(f"entry_k_resolves_Name_sum_squares={entry_resolves_function_name}")
    ok = (
        function_name
        and program_params
        and closure_params
        and closure_env
        and has_math_import
        and body_equal
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
