#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/review-59

echo '$ python3 trusted/py2mpy.py candidate-src/solution.py > regenerated-solution.mpy'
python3 "$scratch/trusted/py2mpy.py" "$scratch/candidate-src/solution.py" \
  > "$scratch/regenerated-solution.mpy"
translate_status=$?
echo "exit=$translate_status"

echo '$ cmp -s regenerated-solution.mpy candidate-src/solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/candidate-src/solution.mpy"
cmp_status=$?
echo "exit=$cmp_status"
if [ "$cmp_status" -ne 0 ]; then
  diff -u "$scratch/candidate-src/solution.mpy" "$scratch/regenerated-solution.mpy" || true
fi

echo '$ sha256sum candidate-src/solution.mpy regenerated-solution.mpy'
sha256sum "$scratch/candidate-src/solution.mpy" "$scratch/regenerated-solution.mpy"
echo "exit=$?"

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
test_status=$?
echo "exit=$test_status"

if [ "$translate_status" -ne 0 ] || [ "$cmp_status" -ne 0 ] || [ "$test_status" -ne 0 ]; then
  exit 1
fi
