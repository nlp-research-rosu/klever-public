#!/usr/bin/env python3
"""Compare the candidate entry point with the trusted canonical AST."""

from __future__ import annotations

import ast
from pathlib import Path


def target(path: Path) -> ast.FunctionDef:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    matches = [
        item
        for item in module.body
        if isinstance(item, ast.FunctionDef) and item.name == "flip_case"
    ]
    assert len(matches) == 1
    return matches[0]


def without_docstring(function: ast.FunctionDef) -> list[ast.stmt]:
    body = function.body
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    return body


canonical = target(Path("/tmp/audit-work/rebuild/canonical.py"))
candidate = target(Path("/tmp/audit-work/rebuild/solution.py"))
signature_equal = ast.dump(canonical.args, include_attributes=False) == ast.dump(
    candidate.args, include_attributes=False
)
behavior_body_equal = ast.dump(
    ast.Module(body=without_docstring(canonical), type_ignores=[]),
    include_attributes=False,
) == ast.dump(
    ast.Module(body=without_docstring(candidate), type_ignores=[]),
    include_attributes=False,
)
print(f"entry_name_equal={canonical.name == candidate.name}")
print(f"signature_ast_equal={signature_equal}")
print(f"behavior_body_ast_equal_after_docstring_removal={behavior_body_equal}")
print(
    "candidate_behavior_ast="
    + ast.dump(
        ast.Module(body=without_docstring(candidate), type_ignores=[]),
        include_attributes=False,
    )
)
if not signature_equal or not behavior_body_equal:
    raise SystemExit(1)
print("SOURCE_FIDELITY_STATUS=PASS")
