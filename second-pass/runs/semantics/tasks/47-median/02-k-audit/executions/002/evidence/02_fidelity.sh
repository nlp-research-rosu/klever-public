#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction

python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$scratch/regenerated-solution.mpy"
translate_status=$?
echo "COMMAND python3 $scratch/py2mpy.py $scratch/solution.py > $scratch/regenerated-solution.mpy"
echo "TRANSLATOR_EXIT=$translate_status"

cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_status=$?
echo "COMMAND cmp -s $scratch/regenerated-solution.mpy $scratch/solution.mpy"
echo "CMP_EXIT=$cmp_status"
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"

python3 /audit-output/evidence/02_differential.py
differential_status=$?
echo "COMMAND python3 /audit-output/evidence/02_differential.py"
echo "DIFFERENTIAL_EXIT=$differential_status"

if [[ $translate_status -ne 0 || $cmp_status -ne 0 ]]; then
  exit 2
fi
exit "$differential_status"
