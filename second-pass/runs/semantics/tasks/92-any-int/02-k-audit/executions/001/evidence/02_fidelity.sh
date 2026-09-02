#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work
evidence=/audit-output/evidence

echo '$ python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy'
python3 /reference/py2mpy.py "$scratch/candidate-src/solution.py" > "$scratch/regenerated-solution.mpy"
translate_status=$?
echo "exit=$translate_status"

echo '$ cmp -s /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate-src/solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/candidate-src/solution.mpy"
cmp_status=$?
echo "exit=$cmp_status"
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/candidate-src/solution.mpy"
if test "$cmp_status" -ne 0; then
  diff -u "$scratch/candidate-src/solution.mpy" "$scratch/regenerated-solution.mpy"
fi

echo '$ python3 /audit-output/evidence/differential_test.py'
python3 "$evidence/differential_test.py"
diff_status=$?
echo "exit=$diff_status"

if test "$translate_status" -eq 0 &&
   test "$cmp_status" -eq 0 &&
   test "$diff_status" -eq 0
then
  exit 0
fi
exit 1
