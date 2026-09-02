#!/usr/bin/env bash
set -u

cd /tmp/audit-work || exit 90

echo '$ python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
translator_status=$?
echo "EXIT_STATUS=$translator_status"

echo '$ cmp -s regenerated-solution.mpy solution.mpy'
cmp -s regenerated-solution.mpy solution.mpy
identity_status=$?
echo "EXIT_STATUS=$identity_status"

echo '$ sha256sum solution.mpy regenerated-solution.mpy'
sha256sum solution.mpy regenerated-solution.mpy
hash_status=$?
echo "EXIT_STATUS=$hash_status"

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
differential_status=$?
echo "EXIT_STATUS=$differential_status"

if [[ "$translator_status" -ne 0 || "$identity_status" -ne 0 ||
      "$hash_status" -ne 0 || "$differential_status" -ne 0 ]]; then
  exit 1
fi
exit 0
