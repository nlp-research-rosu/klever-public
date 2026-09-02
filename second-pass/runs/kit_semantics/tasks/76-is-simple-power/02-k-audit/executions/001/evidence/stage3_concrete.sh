#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/76-is-simple-power

printf '%s\n' '$ python3 AST comparison: submitted solution.py vs concrete_program.py'
python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(
    Path("/tmp/audit-work/76-is-simple-power/solution.py").read_text()
).body[0]
harness = ast.parse(
    Path("/audit-output/evidence/concrete_program.py").read_text()
).body[0]
left = ast.dump(solution, include_attributes=False)
right = ast.dump(harness, include_attributes=False)
print(f"function_ast_identical={left == right}")
if left != right:
    raise SystemExit(1)
PY
printf '%s\n' '[exit 0]'

printf '%s\n' '$ python3 py2mpy.py /audit-output/evidence/concrete_program.py > concrete-audit.mpy'
(
  cd "$scratch"
  python3 py2mpy.py /audit-output/evidence/concrete_program.py > concrete-audit.mpy
)
printf '%s\n' '[exit 0]'

printf '%s\n' '$ krun concrete-audit.mpy --definition runtime-audit-kompiled'
(
  cd "$scratch"
  krun concrete-audit.mpy --definition runtime-audit-kompiled
)
printf '%s\n' '[exit 0]'
