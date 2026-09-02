#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
python3 "$scratch/py2mpy.py" "$scratch/solution.py" >"$scratch/solution.regenerated.mpy"
translate_status=$?
printf 'translator_exit_status=%s\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

cmp "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
cmp_status=$?
printf 'byte_cmp_status=%s\n' "$cmp_status"
sha256sum "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
exit "$cmp_status"
