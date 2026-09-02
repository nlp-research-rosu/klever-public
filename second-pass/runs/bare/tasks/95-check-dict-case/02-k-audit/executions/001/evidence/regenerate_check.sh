#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/candidate-src

python3 "$scratch/py2mpy.py" "$scratch/solution.py" \
  > "$scratch/solution.regenerated.mpy"
translator_status=$?
echo "trusted translator status: $translator_status"

cmp "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
cmp_status=$?
echo "submitted-vs-regenerated cmp status: $cmp_status"

sha256sum "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"

(( translator_status == 0 && cmp_status == 0 ))
