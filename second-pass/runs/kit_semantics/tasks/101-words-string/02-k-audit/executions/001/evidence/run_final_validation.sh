#!/usr/bin/env bash
set -euo pipefail

echo 'COMMAND: parse every reviewer Python script with ast.parse'
python3 - <<'PY'
import ast
from pathlib import Path

scripts = sorted(Path("/audit-output/evidence").glob("*.py"))
for script in scripts:
    ast.parse(script.read_text(), filename=str(script))
print(f"PYTHON_SYNTAX_OK scripts={len(scripts)}")
PY
echo 'EXIT_STATUS: 0'

echo 'COMMAND: bash -n on every reviewer shell script'
for script in /audit-output/evidence/*.sh; do
  bash -n "$script"
done
echo 'SHELL_SYNTAX_OK'
echo 'EXIT_STATUS: 0'

echo 'COMMAND: validate final REVIEW.md markers'
test "$(grep -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
test "$(grep -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1
test "$(tail -n 2 /audit-output/REVIEW.md | sed -n '1p')" = 'VERDICT: PASS'
test "$(tail -n 1 /audit-output/REVIEW.md)" = 'LEGITIMACY: LEGIT'
echo 'FINAL_MARKERS_OK'
echo 'EXIT_STATUS: 0'

echo 'COMMAND: validate referenced evidence files'
for required in \
  /audit-output/evidence/stage1-provenance.log \
  /audit-output/evidence/stage1-generation-record-inspection.log \
  /audit-output/evidence/stage2-program-fidelity.log \
  /audit-output/evidence/stage3-clean-reconstruction.log \
  /audit-output/evidence/stage4-pinning.log \
  /audit-output/evidence/rule-inventory.md \
  /audit-output/evidence/stage6-mutations.log; do
  test -s "$required"
done
echo 'EVIDENCE_FILES_OK'
echo 'EXIT_STATUS: 0'

echo 'COMMAND: validate decisive recorded markers'
grep -q '^#Top$' /audit-output/evidence/stage3-clean-reconstruction.log
grep -q 'SCRIPT_EXIT_STATUS: 0' /audit-output/evidence/stage3-clean-reconstruction.log
grep -q 'MECHANICALLY_EXTRACTED_CONSTRUCTOR_AST_IDENTITY: YES' /audit-output/evidence/stage4-pinning.log
grep -q 'MUTATION_BUILD_RESULT: PASS' /audit-output/evidence/stage6-mutations.log
grep -q 'MUTATION_REJECTION_RESULT: PASS' /audit-output/evidence/stage6-mutations.log
grep -q 'SUMMARY failures=0' /audit-output/evidence/stage1-provenance.log
grep -q 'MISMATCHES=0' /audit-output/evidence/stage2-program-fidelity.log
grep -q 'TOTAL_RECORDS: 1073' /audit-output/evidence/rule-inventory.md
echo 'DECISIVE_MARKERS_OK'
echo 'EXIT_STATUS: 0'

echo 'COMMAND: validate fresh definition locations'
test -d /tmp/audit-work/reconstruction/runtime-fresh-kompiled
test -d /tmp/audit-work/reconstruction/verification-fresh-kompiled
echo 'FRESH_DEFINITIONS_OK'
echo 'EXIT_STATUS: 0'

echo 'FINAL_VALIDATION_OK'
