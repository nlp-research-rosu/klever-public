#!/usr/bin/env bash
set -u

echo 'COMMAND: python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy'
python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
audit_translate_status=$?
echo "EXIT_STATUS: ${audit_translate_status}"

echo 'COMMAND: cmp -s /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy'
cmp -s /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate/solution.mpy
audit_identity_status=$?
echo "EXIT_STATUS: ${audit_identity_status}"

echo 'COMMAND: diff -u /tmp/audit-work/candidate/solution.mpy /tmp/audit-work/regenerated-solution.mpy'
diff -u /tmp/audit-work/candidate/solution.mpy \
  /tmp/audit-work/regenerated-solution.mpy
audit_diff_status=$?
echo "EXIT_STATUS: ${audit_diff_status}"

echo 'COMMAND: python3 /audit-output/evidence/differential.py'
python3 /audit-output/evidence/differential.py
audit_differential_status=$?
echo "EXIT_STATUS: ${audit_differential_status}"

if (( audit_translate_status != 0 || audit_identity_status != 0 || audit_diff_status != 0 )); then
  exit 2
fi
exit "${audit_differential_status}"
