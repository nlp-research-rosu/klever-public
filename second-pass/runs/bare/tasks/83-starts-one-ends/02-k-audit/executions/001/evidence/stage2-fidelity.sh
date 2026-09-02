#!/usr/bin/env bash
set -u

work=/tmp/audit-work/review-83
status=0

echo "command: python3 /reference/py2mpy.py $work/solution.py > $work/regenerated-solution.mpy"
python3 /reference/py2mpy.py "$work/solution.py" > "$work/regenerated-solution.mpy"
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "command: cmp -s $work/regenerated-solution.mpy $work/solution.mpy"
cmp -s "$work/regenerated-solution.mpy" "$work/solution.mpy"
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then
  echo "submitted solution.mpy differs from trusted regeneration"
  diff -u "$work/solution.mpy" "$work/regenerated-solution.mpy" || true
  status=1
else
  echo "byte identity: yes"
fi

echo "command: python3 /audit-output/evidence/differential_test.py"
python3 /audit-output/evidence/differential_test.py
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "script_exit: $status"
exit "$status"
