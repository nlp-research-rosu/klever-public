#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/candidate-src
cd "$work"

for stale in audit-runtime-kompiled audit-verification-kompiled; do
  if test -e "$stale"; then
    echo "ERROR: stale definition exists before clean build: $stale"
    exit 90
  fi
done

run_checked() {
  echo
  echo "$ $*"
  "$@"
  status=$?
  echo "exit_status=$status"
  if test "$status" -ne 0; then
    exit "$status"
  fi
}

run_checked kompile --version
run_checked kprove --version
run_checked krun --version

echo
echo '$ python3 /reference/py2mpy.py /audit-output/evidence/03-clean-rebuild/concrete_checks.py > audit-concrete-checks.mpy'
python3 /reference/py2mpy.py \
  /audit-output/evidence/03-clean-rebuild/concrete_checks.py \
  > audit-concrete-checks.mpy
status=$?
echo "exit_status=$status"
test "$status" -eq 0 || exit "$status"

echo
echo '$ python3 - [mechanically compare candidate and concrete-check function ASTs]'
python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(Path("solution.py").read_text()).body[0]
checks = ast.parse(
    Path("/audit-output/evidence/03-clean-rebuild/concrete_checks.py").read_text()
).body[0]
assert ast.dump(solution, include_attributes=False) == ast.dump(
    checks, include_attributes=False
)
print("function_ast_equal: True")
PY
status=$?
echo "exit_status=$status"
test "$status" -eq 0 || exit "$status"

run_checked kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

run_checked krun solution.mpy --definition audit-runtime-kompiled
run_checked krun audit-concrete-checks.mpy \
  --definition audit-runtime-kompiled

run_checked kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

run_checked kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
