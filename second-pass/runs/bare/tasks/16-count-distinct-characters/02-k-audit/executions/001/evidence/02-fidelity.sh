#!/usr/bin/env bash
set +e

echo '$ python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/generated/solution.mpy'
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/generated/solution.mpy
status=$?
echo "exit=$status"

echo '$ cmp -s /tmp/audit-work/generated/solution.mpy /candidate/solution.mpy'
cmp -s /tmp/audit-work/generated/solution.mpy /candidate/solution.mpy
status=$?
echo "exit=$status"

echo '$ sha256sum /tmp/audit-work/generated/solution.mpy /candidate/solution.mpy'
sha256sum /tmp/audit-work/generated/solution.mpy /candidate/solution.mpy
status=$?
echo "exit=$status"

echo '$ python3 -m py_compile /tmp/audit-work/candidate-src/solution.py'
python3 -m py_compile /tmp/audit-work/candidate-src/solution.py
status=$?
echo "exit=$status"

echo '$ python3 /audit-output/evidence/02-differential.py'
python3 /audit-output/evidence/02-differential.py
status=$?
echo "exit=$status"

exit "$status"
