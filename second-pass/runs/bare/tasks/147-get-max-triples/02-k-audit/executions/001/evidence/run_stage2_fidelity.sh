#!/usr/bin/env bash
set -u
cd /tmp/audit-work/audit147 || exit 99

echo '$ python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy'
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
status=$?
echo "exit_status=$status"

echo '$ cmp -s regenerated-solution.mpy /candidate/solution.mpy'
cmp -s regenerated-solution.mpy /candidate/solution.mpy
status=$?
echo "exit_status=$status"

echo '$ sha256sum regenerated-solution.mpy /candidate/solution.mpy'
sha256sum regenerated-solution.mpy /candidate/solution.mpy
status=$?
echo "exit_status=$status"

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
status=$?
echo "exit_status=$status"
exit "$status"
