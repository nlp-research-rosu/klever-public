#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import ast
from pathlib import Path

candidate = ast.parse(Path("/tmp/audit-work/src/solution.py").read_text())
harness = ast.parse(Path("/audit-output/evidence/concrete_audit.py").read_text())
candidate_function = next(node for node in candidate.body if isinstance(node, ast.FunctionDef))
harness_function = next(node for node in harness.body if isinstance(node, ast.FunctionDef))
if ast.dump(candidate_function, include_attributes=False) != ast.dump(
    harness_function, include_attributes=False
):
    raise SystemExit("harness function differs from submitted solution.py")
print("HARNESS_FUNCTION_AST_IDENTITY=PASS")
PY

python3 /tmp/audit-work/trusted/py2mpy.py \
  /audit-output/evidence/concrete_audit.py \
  > /tmp/audit-work/concrete-audit.mpy

krun /tmp/audit-work/concrete-audit.mpy \
  --definition /tmp/audit-work/src/audit-runtime-kompiled
