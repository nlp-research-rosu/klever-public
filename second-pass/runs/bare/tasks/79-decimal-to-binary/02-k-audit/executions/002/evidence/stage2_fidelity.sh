#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/audit79
evidence=/audit-output/evidence
status=0

echo 'COMMAND: python3 trusted_py2mpy.py solution.py > regenerated-solution.mpy'
python3 "$audit_work/trusted_py2mpy.py" "$audit_work/solution.py" \
  > "$audit_work/regenerated-solution.mpy"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy'
cmp -s "$audit_work/regenerated-solution.mpy" "$audit_work/solution.mpy"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: sha256sum regenerated-solution.mpy solution.mpy'
sha256sum "$audit_work/regenerated-solution.mpy" "$audit_work/solution.mpy"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: differential_test.py --emit-inputs > differential_inputs.json'
python3 "$evidence/differential_test.py" \
  --canonical "$audit_work/canonical.py" \
  --generated "$audit_work/solution.py" \
  --emit-inputs > "$evidence/differential_inputs.json"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo 'COMMAND: differential_test.py --inputs differential_inputs.json'
python3 "$evidence/differential_test.py" \
  --canonical "$audit_work/canonical.py" \
  --generated "$audit_work/solution.py" \
  --inputs "$evidence/differential_inputs.json"
command_status=$?
echo "EXIT_STATUS $command_status"
if (( command_status != 0 )); then status=1; fi

echo "SCRIPT_EXIT_STATUS $status"
exit "$status"
