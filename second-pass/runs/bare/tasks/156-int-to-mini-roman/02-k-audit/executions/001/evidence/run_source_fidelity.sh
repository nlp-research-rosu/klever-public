#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction/candidate

echo '$ python3 ../trusted/py2mpy.py solution.py > regenerated-solution.mpy'
(cd "$work" && python3 ../trusted/py2mpy.py solution.py > regenerated-solution.mpy)
status=$?
echo "EXIT_STATUS=$status"
test "$status" -eq 0 || exit "$status"

echo '$ cmp -s regenerated-solution.mpy solution.mpy'
(cd "$work" && cmp -s regenerated-solution.mpy solution.mpy)
status=$?
echo "EXIT_STATUS=$status"
test "$status" -eq 0 || exit "$status"

echo '$ sha256sum regenerated-solution.mpy solution.mpy'
(cd "$work" && sha256sum regenerated-solution.mpy solution.mpy)
status=$?
echo "EXIT_STATUS=$status"
test "$status" -eq 0 || exit "$status"

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
