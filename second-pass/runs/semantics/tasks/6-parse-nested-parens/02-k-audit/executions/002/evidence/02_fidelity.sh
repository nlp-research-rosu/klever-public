#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction

echo 'COMMAND: python3 py2mpy.py solution.py > solution.regenerated.mpy'
(
  cd "$work" || exit 1
  python3 py2mpy.py solution.py > solution.regenerated.mpy
)
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: cmp -s solution.regenerated.mpy solution.mpy'
cmp -s "$work/solution.regenerated.mpy" "$work/solution.mpy"
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  diff -u "$work/solution.mpy" "$work/solution.regenerated.mpy"
  exit "$status"
fi
sha256sum "$work/solution.mpy" "$work/solution.regenerated.mpy"

echo 'COMMAND: python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
status=$?
echo "EXIT_STATUS: $status"
exit "$status"
