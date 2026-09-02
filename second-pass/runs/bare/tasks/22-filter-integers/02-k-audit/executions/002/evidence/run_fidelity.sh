#!/usr/bin/env bash
set +e
work=/tmp/audit-work/candidate-src

echo '$ python3 /tmp/audit-work/reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/candidate-src/regenerated.mpy'
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/regenerated.mpy
translate_status=$?
echo "TRANSLATOR_EXIT_STATUS=$translate_status"

echo '$ cmp -s /tmp/audit-work/candidate-src/regenerated.mpy /tmp/audit-work/candidate-src/solution.mpy'
cmp -s "$work/regenerated.mpy" "$work/solution.mpy"
cmp_status=$?
echo "BYTE_IDENTITY_EXIT_STATUS=$cmp_status"

echo '$ sha256sum /tmp/audit-work/candidate-src/regenerated.mpy /tmp/audit-work/candidate-src/solution.mpy'
sha256sum "$work/regenerated.mpy" "$work/solution.mpy"
hash_status=$?
echo "HASH_EXIT_STATUS=$hash_status"

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
differential_status=$?
echo "DIFFERENTIAL_EXIT_STATUS=$differential_status"

if (( translate_status || cmp_status || hash_status || differential_status )); then
  exit 1
fi
exit 0
