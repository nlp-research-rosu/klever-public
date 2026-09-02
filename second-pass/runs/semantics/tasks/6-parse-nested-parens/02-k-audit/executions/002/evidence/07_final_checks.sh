#!/usr/bin/env bash
set -u

echo 'COMMAND: verify REVIEW.md seven stages and exact terminal markers'
for stage in 1 2 3 4 5 6 7; do
  rg -q "^## ${stage}\\." /audit-output/REVIEW.md || exit 10
done
test "$(tail -n 2 /audit-output/REVIEW.md)" = $'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: syntax-check all reviewer shell scripts'
for script in /audit-output/evidence/*.sh; do
  bash -n "$script" || exit 20
done
echo 'EXIT_STATUS: 0'

echo 'COMMAND: AST-parse all reviewer Python scripts without writing caches'
python3 - <<'PY'
import ast
from pathlib import Path

paths = sorted(Path("/audit-output/evidence").glob("*.py"))
for path in paths:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print(f"PYTHON_SCRIPTS_PARSED={len(paths)}")
PY
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: verify core evidence success/failure signals'
rg -q 'PROVENANCE_CHECK=PASS' /audit-output/evidence/01_provenance.log
rg -q 'DIFFERENTIAL_VALID_DOMAIN=PASS' /audit-output/evidence/02_fidelity.log
test "$(rg -c '^#Top$' /audit-output/evidence/03_reconstruct.log)" -eq 2
rg -q 'CLOSURE_BINDING_BODY_IDENTITY=PASS' /audit-output/evidence/04_adequacy.log
rg -q 'BODY_SENSITIVITY=EXPECTED_PROOF_FAILURE' /audit-output/evidence/04_body_sensitivity.log
rg -q 'EXHAUSTIVE_INVENTORY=PASS' /audit-output/evidence/05_inventory.log
rg -q 'NONVACUITY=EXPECTED_FALSE_CLAIM_FAILURE' /audit-output/evidence/06_nonvacuity.log
status=$?
echo "EXIT_STATUS: $status"
exit "$status"
