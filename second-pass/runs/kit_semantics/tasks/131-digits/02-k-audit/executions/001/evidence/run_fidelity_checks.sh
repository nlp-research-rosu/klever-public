#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/source || exit 90

echo '$ python3 /audit-output/evidence/differential_test.py --list-inputs > /audit-output/evidence/differential_inputs.txt'
python3 /audit-output/evidence/differential_test.py --list-inputs \
  > /audit-output/evidence/differential_inputs.txt
inputs_status=$?
echo "EXIT_STATUS=$inputs_status"
echo '$ wc -l /audit-output/evidence/differential_inputs.txt'
wc -l /audit-output/evidence/differential_inputs.txt
echo '$ sha256sum /audit-output/evidence/differential_inputs.txt'
sha256sum /audit-output/evidence/differential_inputs.txt

echo '$ python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy'
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
echo "EXIT_STATUS=$translate_status"

echo '$ cmp -s regenerated-solution.mpy solution.mpy'
cmp -s regenerated-solution.mpy solution.mpy
cmp_status=$?
echo "EXIT_STATUS=$cmp_status"

echo '$ sha256sum regenerated-solution.mpy solution.mpy'
sha256sum regenerated-solution.mpy solution.mpy
hash_status=$?
echo "EXIT_STATUS=$hash_status"

echo '$ python3 /audit-output/evidence/differential_test.py --input-file /audit-output/evidence/differential_inputs.txt'
python3 /audit-output/evidence/differential_test.py \
  --input-file /audit-output/evidence/differential_inputs.txt
diff_status=$?
echo "EXIT_STATUS=$diff_status"

test "$inputs_status" -eq 0 \
  && test "$translate_status" -eq 0 \
  && test "$cmp_status" -eq 0 \
  && test "$hash_status" -eq 0 \
  && test "$diff_status" -eq 0
