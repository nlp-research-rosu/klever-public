#!/usr/bin/env bash
set -u
cd /tmp/audit-work/audit147 || exit 99
overall=0

echo '$ python3 /audit-output/evidence/claim_adequacy_check.py'
python3 /audit-output/evidence/claim_adequacy_check.py
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi

echo '$ krun /audit-output/evidence/div-positive-denominator.mpy --definition fresh-runtime-kompiled -cN=1'
krun /audit-output/evidence/div-positive-denominator.mpy \
  --definition fresh-runtime-kompiled -cN=1
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi
echo "$ python3 -c 'print(-7 // 3)'"
python3 -c 'print(-7 // 3)'
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi

echo '$ krun /audit-output/evidence/div-negative-denominator.mpy --definition fresh-runtime-kompiled -cN=1'
krun /audit-output/evidence/div-negative-denominator.mpy \
  --definition fresh-runtime-kompiled -cN=1
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi
echo "$ python3 -c 'print(7 // -3)'"
python3 -c 'print(7 // -3)'
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi

echo "overall_exit_status=$overall"
exit "$overall"
