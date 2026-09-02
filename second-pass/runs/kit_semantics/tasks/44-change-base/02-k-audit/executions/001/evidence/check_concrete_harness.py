#!/usr/bin/env python3
import ast
from pathlib import Path


solution = ast.parse(
    Path("/tmp/audit-work/44-change-base/solution.py").read_text()
)
harness = ast.parse(
    Path("/tmp/audit-work/44-change-base/concrete_actual.py").read_text()
)
solution_function = solution.body[0]
harness_function = harness.body[0]
equal = ast.dump(solution_function, include_attributes=False) == ast.dump(
    harness_function, include_attributes=False
)
print(f"solution_first_node={type(solution_function).__name__}")
print(f"harness_first_node={type(harness_function).__name__}")
print(f"function_ast_identical={equal}")
raise SystemExit(0 if equal else 1)
