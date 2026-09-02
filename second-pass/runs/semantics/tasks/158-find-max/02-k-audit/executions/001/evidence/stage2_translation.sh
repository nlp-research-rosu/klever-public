#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
regenerated="$scratch/solution.regenerated.mpy"

python3 /reference/py2mpy.py "$scratch/solution.py" > "$regenerated"
translate_status=$?
printf 'trusted translator exit: %d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

cmp -s "$regenerated" "$scratch/solution.mpy"
cmp_status=$?
printf 'byte-identity cmp exit: %d\n' "$cmp_status"
sha256sum "$scratch/solution.py" "$scratch/solution.mpy" "$regenerated"

if (( cmp_status != 0 )); then
  diff -u "$scratch/solution.mpy" "$regenerated" || true
fi
exit "$cmp_status"
