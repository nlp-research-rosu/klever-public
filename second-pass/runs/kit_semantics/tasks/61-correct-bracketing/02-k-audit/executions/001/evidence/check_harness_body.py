#!/usr/bin/env python3
"""Mechanically check that the concrete K harness embeds solution.py exactly."""

import ast
from pathlib import Path


def function_ast(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "correct_bracketing"
    )
    return ast.dump(function, include_attributes=False)


solution = function_ast(Path("/tmp/audit-work/fresh/solution.py"))
harness = function_ast(Path("/audit-output/evidence/concrete_harness.py"))
print(f"exact_function_ast_match={solution == harness}")
raise SystemExit(0 if solution == harness else 1)
