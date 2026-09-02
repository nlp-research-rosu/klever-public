#!/usr/bin/env bash
set -u

status=0
trusted_translator=/tmp/audit-work/reference-src/py2mpy.py
submitted_py=/tmp/audit-work/candidate-src/solution.py
submitted_mpy=/tmp/audit-work/candidate-src/solution.mpy
regenerated=/tmp/audit-work/regenerated-solution.mpy

echo '$ python3 /tmp/audit-work/reference-src/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy'
python3 "$trusted_translator" "$submitted_py" > "$regenerated"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ cmp -s /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate-src/solution.mpy'
cmp -s "$regenerated" "$submitted_mpy"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ sha256sum regenerated and submitted solution.mpy'
sha256sum "$regenerated" "$submitted_mpy"

echo '$ diff -u submitted solution.mpy regenerated solution.mpy'
diff -u "$submitted_mpy" "$regenerated"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo "overall_exit=$status"
exit "$status"
