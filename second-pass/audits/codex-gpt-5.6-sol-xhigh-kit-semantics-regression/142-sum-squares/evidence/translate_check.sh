#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/142-sum-squares
python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$scratch/solution.regenerated.mpy"
translator_status=$?
if [[ $translator_status -ne 0 ]]; then
  echo "TRANSLATOR_EXIT=$translator_status"
  exit "$translator_status"
fi

cmp "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
cmp_status=$?
sha256sum "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
echo "BYTE_IDENTITY_CMP_EXIT=$cmp_status"
exit "$cmp_status"
