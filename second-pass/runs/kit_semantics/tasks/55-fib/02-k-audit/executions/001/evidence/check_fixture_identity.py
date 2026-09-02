#!/usr/bin/env python3
"""Require the concrete K fixture to contain the submitted function exactly."""

import ast
from pathlib import Path


solution = ast.parse(
    Path("/tmp/audit-work/fib-audit/solution.py").read_text(encoding="utf-8")
)
fixture = ast.parse(
    Path("/audit-output/evidence/concrete_audit.py").read_text(encoding="utf-8")
)
solution_function = next(node for node in solution.body if isinstance(node, ast.FunctionDef))
fixture_function = next(node for node in fixture.body if isinstance(node, ast.FunctionDef))
assert ast.dump(solution_function, include_attributes=False) == ast.dump(
    fixture_function, include_attributes=False
)
print("AST FUNCTION IDENTITY: solution.py == concrete_audit.py fib definition")
