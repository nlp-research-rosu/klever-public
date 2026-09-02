#!/usr/bin/env python3
"""Require the harness function AST to equal the submitted function AST."""

import ast
from pathlib import Path


def first_function(path: Path) -> ast.FunctionDef:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1:
        raise AssertionError(f"{path}: expected one top-level function")
    return functions[0]


candidate = first_function(Path("/tmp/audit-work/anti-shuffle-audit/solution.py"))
harness = first_function(Path("/audit-output/evidence/08_concrete_harness.py"))
candidate_dump = ast.dump(candidate, include_attributes=False)
harness_dump = ast.dump(harness, include_attributes=False)
print(f"candidate_function={candidate.name}")
print(f"harness_function={harness.name}")
print(f"ast_byte_equal={candidate_dump.encode() == harness_dump.encode()}")
if candidate_dump != harness_dump:
    raise SystemExit(1)
