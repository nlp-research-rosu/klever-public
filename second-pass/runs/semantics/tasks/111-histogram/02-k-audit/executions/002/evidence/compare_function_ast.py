#!/usr/bin/env python3
"""Require the concrete K harness to execute the exact submitted function."""

import ast
from pathlib import Path


def first_function(path: Path) -> ast.FunctionDef:
    tree = ast.parse(path.read_text(), filename=str(path))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert len(functions) == 1, (path, len(functions))
    return functions[0]


candidate = first_function(Path("/tmp/audit-work/111-histogram/solution.py"))
harness = first_function(Path("/audit-output/evidence/k_concrete_audit.py"))
assert ast.dump(candidate, include_attributes=False) == ast.dump(
    harness, include_attributes=False
)
print("CONCRETE_HARNESS_FUNCTION_AST_IDENTICAL=True")
