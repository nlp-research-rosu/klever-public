#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/integrity_check.py'
python3 /audit-output/evidence/integrity_check.py
integrity_status=$?
printf 'EXIT_STATUS: %s\n' "$integrity_status"

printf '%s\n' 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
printf 'EXIT_STATUS: %s\n' "$translate_status"

printf '%s\n' 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy'
cmp -s regenerated-solution.mpy solution.mpy
cmp_status=$?
printf 'EXIT_STATUS: %s\n' "$cmp_status"
sha256sum regenerated-solution.mpy solution.mpy

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/differential_test.py --canonical /reference/canonical.py --solution /tmp/audit-work/142-sum-squares-audit/solution.py --inputs-out /audit-output/evidence/differential-inputs-results.jsonl'
python3 /audit-output/evidence/differential_test.py \
  --canonical /reference/canonical.py \
  --solution /tmp/audit-work/142-sum-squares-audit/solution.py \
  --inputs-out /audit-output/evidence/differential-inputs-results.jsonl
differential_status=$?
printf 'EXIT_STATUS: %s\n' "$differential_status"

if (( integrity_status == 2 || translate_status != 0 || cmp_status != 0 || differential_status != 0 )); then
  exit 1
fi
exit 0
