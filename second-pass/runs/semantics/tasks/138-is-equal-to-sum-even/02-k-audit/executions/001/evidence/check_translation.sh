#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/review-138 || exit 99

echo "COMMAND: python3 /reference/py2mpy.py solution.py"
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
status=$?
echo "EXIT_STATUS: $status"

echo "COMMAND: cmp -s regenerated-solution.mpy solution.mpy"
cmp -s regenerated-solution.mpy solution.mpy
status=$?
echo "EXIT_STATUS: $status"

echo "COMMAND: sha256sum regenerated-solution.mpy solution.mpy"
sha256sum regenerated-solution.mpy solution.mpy
echo "EXIT_STATUS: ${PIPESTATUS[0]}"

echo "COMMAND: diff -u solution.mpy regenerated-solution.mpy"
diff -u solution.mpy regenerated-solution.mpy
echo "EXIT_STATUS: $?"
