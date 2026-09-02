#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/scratch

python3 "$scratch/py2mpy.py" "$scratch/solution.py" \
  >"$scratch/solution.regenerated.mpy"
cmp "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
echo "TRANSLATION_BYTE_IDENTITY=PASS"
sha256sum "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
