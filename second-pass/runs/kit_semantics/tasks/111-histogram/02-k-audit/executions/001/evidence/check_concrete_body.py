#!/usr/bin/env python3
"""Require the reviewer concrete test to embed the exact submitted function."""

import ast
from pathlib import Path


def first_function(path: str) -> ast.FunctionDef:
    module = ast.parse(Path(path).read_text(encoding="utf-8"), filename=path)
    node = module.body[0]
    assert isinstance(node, ast.FunctionDef)
    return node


submitted = first_function("/tmp/audit-work/111-histogram-audit/solution.py")
concrete = first_function("/audit-output/evidence/concrete_semantics_audit.py")
assert ast.dump(submitted, include_attributes=False) == ast.dump(
    concrete, include_attributes=False
)
print("reviewer concrete test embeds the submitted histogram AST exactly: yes")
