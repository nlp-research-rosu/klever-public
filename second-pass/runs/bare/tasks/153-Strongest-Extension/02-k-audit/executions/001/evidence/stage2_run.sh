#!/usr/bin/env bash
set -u
status=0

echo '$ python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy'
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ cmp -s regenerated-solution.mpy submitted solution.mpy'
cmp -s /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ sha256sum regenerated and submitted MPY'
sha256sum /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo "stage2_exit=$status"
exit "$status"
