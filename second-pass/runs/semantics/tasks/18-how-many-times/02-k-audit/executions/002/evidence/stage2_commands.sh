#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 90

echo '$ python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
echo "exit_status=$translate_status"

echo '$ cmp regenerated-solution.mpy solution.mpy'
cmp regenerated-solution.mpy solution.mpy
cmp_status=$?
echo "exit_status=$cmp_status"

echo '$ sha256sum solution.py solution.mpy regenerated-solution.mpy canonical.py'
sha256sum solution.py solution.mpy regenerated-solution.mpy canonical.py
hash_status=$?
echo "exit_status=$hash_status"

echo '$ python3 /audit-output/evidence/differential.py'
python3 /audit-output/evidence/differential.py
differential_status=$?
echo "exit_status=$differential_status"

if (( translate_status != 0 || cmp_status != 0 || hash_status != 0 )); then
  exit 2
fi
exit "$differential_status"
