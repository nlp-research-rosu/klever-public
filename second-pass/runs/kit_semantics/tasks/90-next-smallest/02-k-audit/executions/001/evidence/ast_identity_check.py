#!/usr/bin/env python3
import ast
import sys
from pathlib import Path


def first_function(path: str):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef))


left = ast.dump(first_function(sys.argv[1]), include_attributes=False)
right = ast.dump(first_function(sys.argv[2]), include_attributes=False)
print(f"function_ast_identity={left == right}")
if left != right:
    print("LEFT", left)
    print("RIGHT", right)
    raise SystemExit(1)
