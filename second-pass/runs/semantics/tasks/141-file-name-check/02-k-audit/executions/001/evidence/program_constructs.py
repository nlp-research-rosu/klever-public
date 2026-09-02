#!/usr/bin/env python3
"""Inventory Python constructs and translator-emitted K constructors."""

from __future__ import annotations

import ast
import re
from collections import Counter
from pathlib import Path


source = Path("/tmp/audit-work/141-file-name-check/solution.py").read_text(
    encoding="utf-8"
)
mpy = Path(
    "/tmp/audit-work/141-file-name-check/regenerated-solution.mpy"
).read_text(encoding="utf-8")
tree = ast.parse(source)

nodes = Counter(type(node).__name__ for node in ast.walk(tree))
calls = []
attributes = []
operators = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            calls.append(f".{node.func.attr}")
    if isinstance(node, ast.Attribute):
        attributes.append(node.attr)
    if isinstance(
        node,
        (
            ast.operator,
            ast.unaryop,
            ast.boolop,
            ast.cmpop,
        ),
    ):
        operators.append(type(node).__name__)

constructors = Counter(re.findall(r"\b([A-Z][A-Za-z0-9]*)\s*\(", mpy))

print("PYTHON_AST_NODES")
for name, count in sorted(nodes.items()):
    print(f"{name} {count}")
print("CALLS")
for name, count in sorted(Counter(calls).items()):
    print(f"{name} {count}")
print("ATTRIBUTES")
for name, count in sorted(Counter(attributes).items()):
    print(f"{name} {count}")
print("OPERATORS")
for name, count in sorted(Counter(operators).items()):
    print(f"{name} {count}")
print("MPY_CONSTRUCTORS")
for name, count in sorted(constructors.items()):
    print(f"{name} {count}")
