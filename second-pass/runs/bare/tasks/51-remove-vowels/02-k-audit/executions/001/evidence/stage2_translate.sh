#!/usr/bin/env bash
set -u

scratch_root=/tmp/audit-work
python3 "$scratch_root/trusted/py2mpy.py" \
  "$scratch_root/candidate-src/solution.py" \
  > "$scratch_root/regenerated-solution.mpy"
translate_status=$?
printf 'translator exit=%d\n' "$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

cmp -s \
  "$scratch_root/regenerated-solution.mpy" \
  "$scratch_root/candidate-src/solution.mpy"
cmp_status=$?
printf 'byte_identity cmp exit=%d\n' "$cmp_status"
sha256sum \
  "$scratch_root/regenerated-solution.mpy" \
  "$scratch_root/candidate-src/solution.mpy"
exit "$cmp_status"
