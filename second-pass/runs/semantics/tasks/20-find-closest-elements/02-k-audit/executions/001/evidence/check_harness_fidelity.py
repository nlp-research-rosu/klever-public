#!/usr/bin/env python3
"""Check that the K concrete harness embeds the exact submitted function AST."""

import ast
from pathlib import Path


def function_node(path: Path) -> ast.FunctionDef:
    module = ast.parse(path.read_text(), filename=str(path))
    functions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
    if not functions:
        raise RuntimeError(f"no function in {path}")
    return functions[0]


solution = function_node(Path("/tmp/audit-work/reconstruction/solution.py"))
harness = function_node(Path("/audit-output/evidence/concrete_harness.py"))
same = ast.dump(solution, include_attributes=False) == ast.dump(harness, include_attributes=False)
print(f"function_ast_identity={same}")
if not same:
    print("solution_ast=" + ast.dump(solution, include_attributes=False))
    print("harness_ast=" + ast.dump(harness, include_attributes=False))
raise SystemExit(0 if same else 1)
