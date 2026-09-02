#!/usr/bin/env python3
"""Verify the function embedded in the reviewer K tests is the candidate function."""

from __future__ import annotations

import ast
from pathlib import Path


def first_function(path: Path) -> ast.FunctionDef:
    module = ast.parse(path.read_text(), filename=str(path))
    function = module.body[0]
    if not isinstance(function, ast.FunctionDef):
        raise TypeError(f"first statement in {path} is not a function")
    return function


candidate = first_function(Path("/candidate/solution.py"))
reviewer = first_function(Path("/audit-output/evidence/auditor_concrete_tests.py"))
candidate_dump = ast.dump(candidate, include_attributes=False)
reviewer_dump = ast.dump(reviewer, include_attributes=False)
print(f"candidate_function_ast_sha256_input_length={len(candidate_dump)}")
print(f"reviewer_function_ast_sha256_input_length={len(reviewer_dump)}")
print(f"function_ast_identical={candidate_dump == reviewer_dump}")
raise SystemExit(0 if candidate_dump == reviewer_dump else 1)
