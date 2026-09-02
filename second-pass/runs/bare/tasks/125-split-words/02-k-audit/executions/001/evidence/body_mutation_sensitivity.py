#!/usr/bin/env python3
"""Confirm that a one-token body mutation changes behavior and AST identity."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from typing import Callable


ORIGINAL_PY = Path("/tmp/audit-work/fresh/candidate/solution.py")
MUTATED_PY = Path("/tmp/audit-work/fresh/generated/body_mutated_solution.py")
MUTATED_MPY = Path("/tmp/audit-work/fresh/generated/body_mutated_solution.mpy")
VERIFICATION = Path("/tmp/audit-work/fresh/candidate/verification.k")
TOKEN_RE = re.compile(
    r'\.Exprs|\.Stmts|"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z_0-9]*|-?[0-9]+|[(),]'
)


def load_entry(path: Path, name: str) -> Callable[[str], object]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "split_words")


def extract_solution_ast_rhs(source: str) -> str:
    marker_index = source.index("rule solutionAST =>")
    module_index = source.index("Module(", marker_index)
    in_string = False
    escaped = False
    depth = 0
    for index in range(module_index, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return source[module_index : index + 1]
    raise ValueError("unterminated solutionAST RHS")


def main() -> int:
    original = load_entry(ORIGINAL_PY, "original_solution")
    mutated = load_entry(MUTATED_PY, "mutated_solution")
    changed_cases = []
    for value in ("", "a", "z", "az", "abcdef"):
        original_result = original(value)
        mutated_result = mutated(value)
        changed = original_result != mutated_result
        if changed:
            changed_cases.append(value)
        print(
            f"INPUT={value!r} ORIGINAL={original_result!r} "
            f"MUTATED={mutated_result!r} CHANGED={changed}"
        )

    mutated_tokens = TOKEN_RE.findall(MUTATED_MPY.read_text(encoding="utf-8"))
    rhs_tokens = [
        token
        for token in TOKEN_RE.findall(
            extract_solution_ast_rhs(VERIFICATION.read_text(encoding="utf-8"))
        )
        if token not in {".Exprs", ".Stmts"}
    ]
    identity = mutated_tokens == rhs_tokens
    first_difference = None
    for index, (mutated_token, proof_token) in enumerate(
        zip(mutated_tokens, rhs_tokens)
    ):
        if mutated_token != proof_token:
            first_difference = (index, mutated_token, proof_token)
            break
    print("CHANGED_CASES:", changed_cases)
    print("MUTATED_AST_MATCHES_SOLUTION_AST:", identity)
    print("FIRST_AST_DIFFERENCE:", first_difference)
    return 0 if changed_cases and not identity else 1


if __name__ == "__main__":
    raise SystemExit(main())
