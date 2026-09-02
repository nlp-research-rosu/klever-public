#!/usr/bin/env bash
set -u

root=/tmp/audit-work/37-sort-even-audit
runtime=$root/reconstruction-fresh/runtime-kompiled
evidence=/audit-output/evidence
status=0

echo '$ python3 /audit-output/evidence/generate_k_differential.py'
python3 "$evidence/generate_k_differential.py"
generator_status=$?
echo "exit=$generator_status"
status=$((status | generator_status))

echo '$ python3 /tmp/audit-work/37-sort-even-audit/trusted/py2mpy.py /audit-output/evidence/k-differential-tests.py > /audit-output/evidence/k-differential-tests.mpy'
python3 "$root/trusted/py2mpy.py" "$evidence/k-differential-tests.py" \
  > "$evidence/k-differential-tests.mpy"
translator_status=$?
echo "exit=$translator_status"
status=$((status | translator_status))

echo '$ python3 /audit-output/evidence/k-differential-tests.py'
python3 "$evidence/k-differential-tests.py"
python_status=$?
echo "exit=$python_status"
status=$((status | python_status))

echo '$ krun /audit-output/evidence/k-differential-tests.mpy --definition /tmp/audit-work/37-sort-even-audit/reconstruction-fresh/runtime-kompiled --output none'
krun "$evidence/k-differential-tests.mpy" \
  --definition "$runtime" \
  --output none
k_status=$?
echo "exit=$k_status"
status=$((status | k_status))

echo "stage7_k_differential_exit=$status"
exit "$status"
