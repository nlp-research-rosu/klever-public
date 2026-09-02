#!/usr/bin/env bash
set -euo pipefail
cd /tmp/audit-work/12-longest-audit

echo '$ python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy'
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
echo '$ cmp regenerated-solution.mpy solution.mpy'
cmp regenerated-solution.mpy solution.mpy
echo "solution_mpy_cmp_exit=$?"
sha256sum regenerated-solution.mpy solution.mpy

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py

echo 'SCRIPT_EXIT_STATUS=0'
