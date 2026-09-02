#!/usr/bin/env python3
"""Require the reviewer concrete harness to contain the submitted function AST."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def first_function(path: Path) -> ast.FunctionDef:
    tree = ast.parse(path.read_text(), filename=str(path))
    for statement in tree.body:
        if isinstance(statement, ast.FunctionDef):
            return statement
    raise RuntimeError(f"no function in {path}")


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} SOLUTION HARNESS")
        return 64
    solution = first_function(Path(sys.argv[1]))
    harness = first_function(Path(sys.argv[2]))
    same = ast.dump(solution, include_attributes=False) == ast.dump(
        harness, include_attributes=False
    )
    print(f"function_ast_identical={same}")
    print(ast.dump(solution, include_attributes=False))
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
