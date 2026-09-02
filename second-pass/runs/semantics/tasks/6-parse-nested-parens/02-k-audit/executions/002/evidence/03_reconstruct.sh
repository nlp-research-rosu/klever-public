#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
cd "$work" || exit 1
export PATH="/home/agent/.nix-profile/bin:$PATH"

run_required() {
  echo "COMMAND: $*"
  "$@"
  status=$?
  echo "EXIT_STATUS: $status"
  if [ "$status" -ne 0 ]; then
    exit "$status"
  fi
}

echo 'COMMAND: verify audit_concrete.py function AST equals solution.py function AST'
python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(Path("solution.py").read_text(encoding="utf-8"))
harness = ast.parse(Path("audit_concrete.py").read_text(encoding="utf-8"))
solution_function = next(node for node in solution.body if isinstance(node, ast.FunctionDef))
harness_function = next(node for node in harness.body if isinstance(node, ast.FunctionDef))
assert ast.dump(solution_function, include_attributes=False) == ast.dump(
    harness_function, include_attributes=False
)
print("FUNCTION_AST_IDENTITY=PASS")
PY
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: python3 py2mpy.py audit_concrete.py > audit_concrete.mpy'
python3 py2mpy.py audit_concrete.py > audit_concrete.mpy
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

run_required kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

run_required krun audit_concrete.mpy \
  --definition audit-runtime-kompiled \
  --output none

run_required kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

run_required kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.parse-loop \
  --output pretty

# The target uses the loop claim as a circularity, so prove the complete spec.
# A single #Top here is success for the conjunction of both selected claims.
run_required kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --output pretty
