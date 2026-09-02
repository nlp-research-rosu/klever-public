#!/usr/bin/env python3
"""Compare the trusted and submitted Python entry-point ASTs."""

import ast
from pathlib import Path


def entry_ast(path: Path) -> ast.FunctionDef:
    module = ast.parse(path.read_text(), filename=str(path))
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == "starts_one_ends":
            return node
    raise RuntimeError(f"missing starts_one_ends in {path}")


trusted = ast.dump(entry_ast(Path("/reference/canonical.py")), include_attributes=False)
submitted = ast.dump(entry_ast(Path("/candidate/solution.py")), include_attributes=False)
print(f"entry_ast_equal={trusted == submitted}")
print(f"trusted_ast={trusted}")
print(f"submitted_ast={submitted}")
raise SystemExit(0 if trusted == submitted else 1)
