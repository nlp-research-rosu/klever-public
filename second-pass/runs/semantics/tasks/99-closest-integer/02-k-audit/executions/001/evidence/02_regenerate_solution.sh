#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/99-closest-integer-audit
python3 "$scratch/trusted/py2mpy.py" \
  "$scratch/candidate/solution.py" \
  > "$scratch/regenerated-solution.mpy"
translate_status=$?
printf 'translator status: %d\n' "$translate_status"

printf '\nSubmitted and regenerated hashes:\n'
sha256sum \
  "$scratch/candidate/solution.mpy" \
  "$scratch/regenerated-solution.mpy"

cmp "$scratch/candidate/solution.mpy" "$scratch/regenerated-solution.mpy"
cmp_status=$?
printf 'byte-identity cmp status: %d\n' "$cmp_status"

if [[ "$translate_status" -ne 0 || "$cmp_status" -ne 0 ]]; then
  exit 1
fi
