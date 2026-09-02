#!/usr/bin/env python3
"""Check that the K concrete harness embeds the submitted function verbatim."""

import ast
from pathlib import Path


def target_function(path: Path) -> ast.FunctionDef:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "sum_squares"
    ]
    if len(matches) != 1:
        raise RuntimeError(f"{path}: expected exactly one sum_squares definition")
    return matches[0]


solution = target_function(Path("/tmp/audit-work/reconstruction/solution.py"))
harness = target_function(Path("/audit-output/evidence/k_concrete_tests.py"))
solution_dump = ast.dump(solution, include_attributes=False)
harness_dump = ast.dump(harness, include_attributes=False)
print(f"solution_function_ast={solution_dump}")
print(f"harness_function_ast={harness_dump}")
print(f"function_ast_identical={solution_dump == harness_dump}")
raise SystemExit(0 if solution_dump == harness_dump else 1)
