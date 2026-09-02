#!/usr/bin/env bash
set -u

work=/tmp/audit-work/106-f

echo 'COMMAND: trusted py2mpy.py regenerates solution.mpy'
python3 "$work/reference/py2mpy.py" "$work/source/solution.py" > "$work/build/regenerated-solution.mpy"
translator_status=$?
echo "EXIT_STATUS: $translator_status"

echo 'COMMAND: cmp submitted and independently regenerated solution.mpy'
cmp "$work/source/solution.mpy" "$work/build/regenerated-solution.mpy"
cmp_status=$?
echo "EXIT_STATUS: $cmp_status"

echo 'COMMAND: sha256sum submitted and regenerated solution.mpy'
sha256sum "$work/source/solution.mpy" "$work/build/regenerated-solution.mpy"
hash_status=$?
echo "EXIT_STATUS: $hash_status"

echo 'COMMAND: python3 /audit-output/evidence/01_differential_test.py'
python3 /audit-output/evidence/01_differential_test.py
diff_status=$?
echo "EXIT_STATUS: $diff_status"

if [ "$translator_status" -eq 0 ] && [ "$cmp_status" -eq 0 ] && [ "$diff_status" -eq 0 ]; then
  exit 0
fi
exit 1
