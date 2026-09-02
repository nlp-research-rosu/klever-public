#!/usr/bin/env python3
"""Check that the concrete K harness embeds the exact candidate function AST."""

import ast
import sys
from pathlib import Path


def first_function(path: Path) -> ast.FunctionDef:
    tree = ast.parse(path.read_text(), filename=str(path))
    node = tree.body[0]
    assert isinstance(node, ast.FunctionDef)
    return node


left = ast.dump(first_function(Path(sys.argv[1])), include_attributes=False)
right = ast.dump(first_function(Path(sys.argv[2])), include_attributes=False)
print("FUNCTION_AST_IDENTICAL", left == right)
raise SystemExit(0 if left == right else 1)
