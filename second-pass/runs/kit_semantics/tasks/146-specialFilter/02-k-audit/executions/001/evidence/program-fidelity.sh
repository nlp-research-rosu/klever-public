#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work

echo 'COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
echo "EXIT: $translate_status"

echo 'COMMAND: cmp regenerated-solution.mpy submitted-solution.mpy'
cmp regenerated-solution.mpy submitted-solution.mpy
cmp_status=$?
echo "EXIT: $cmp_status"
sha256sum solution.py regenerated-solution.mpy submitted-solution.mpy

echo 'COMMAND: python3 /audit-output/evidence/differential.py'
python3 /audit-output/evidence/differential.py
differential_status=$?
echo "EXIT: $differential_status"

exit $((translate_status || cmp_status || differential_status))
