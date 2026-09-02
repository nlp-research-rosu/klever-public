#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/candidate-src

echo '$ python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy'
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
echo "exit_status=$translate_status"
test "$translate_status" -eq 0 || exit "$translate_status"

echo '$ cmp regenerated-solution.mpy solution.mpy'
cmp regenerated-solution.mpy solution.mpy
cmp_status=$?
echo "exit_status=$cmp_status"
test "$cmp_status" -eq 0 || exit "$cmp_status"

echo '$ sha256sum solution.py solution.mpy regenerated-solution.mpy'
sha256sum solution.py solution.mpy regenerated-solution.mpy
hash_status=$?
echo "exit_status=$hash_status"
test "$hash_status" -eq 0 || exit "$hash_status"

echo '$ python3 /audit-output/evidence/02-program-fidelity/differential_test.py'
python3 /audit-output/evidence/02-program-fidelity/differential_test.py
diff_status=$?
echo "exit_status=$diff_status"
exit "$diff_status"
