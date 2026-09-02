#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/43-pairs-sum-to-zero
echo 'COMMAND: python3 trusted/py2mpy.py candidate/solution.py > regenerated.mpy'
python3 "$scratch/trusted/py2mpy.py" \
  "$scratch/candidate/solution.py" > "$scratch/regenerated.mpy"
status=$?
echo "TRANSLATOR_EXIT_STATUS: $status"
if (( status != 0 )); then
  exit "$status"
fi

echo 'COMMAND: cmp -s regenerated.mpy candidate/solution.mpy'
cmp -s "$scratch/regenerated.mpy" "$scratch/candidate/solution.mpy"
status=$?
echo "CMP_EXIT_STATUS: $status"
sha256sum "$scratch/regenerated.mpy" "$scratch/candidate/solution.mpy"
exit "$status"
