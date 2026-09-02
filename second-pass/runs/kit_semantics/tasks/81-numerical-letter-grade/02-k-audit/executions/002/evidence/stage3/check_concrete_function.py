#!/usr/bin/env python3
"""Require the concrete audit wrapper to contain the exact candidate function AST."""

import ast
from pathlib import Path


candidate = ast.parse(
    Path("/tmp/audit-work/candidate-src/solution.py").read_text(encoding="utf-8")
).body[0]
wrapper = ast.parse(
    Path("/audit-output/evidence/stage3/concrete_audit.py").read_text(encoding="utf-8")
).body[0]
if ast.dump(candidate, include_attributes=False) != ast.dump(
    wrapper, include_attributes=False
):
    raise SystemExit("concrete wrapper function differs from candidate solution.py")
print("CONCRETE_FUNCTION_AST EXACT_MATCH")
