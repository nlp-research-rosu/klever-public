#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/30-get-positive
generated="$scratch/independently-regenerated-solution.mpy"
python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$generated"
translate_status=$?
if [ "$translate_status" -ne 0 ]; then
  printf 'TRANSLATOR_EXIT_STATUS: %s\n' "$translate_status"
  exit "$translate_status"
fi

cmp "$generated" /candidate/solution.mpy
compare_status=$?
printf 'COMMAND: python3 %s/py2mpy.py %s/solution.py > %s\n' \
  "$scratch" "$scratch" "$generated"
printf 'TRANSLATOR_EXIT_STATUS: %s\n' "$translate_status"
printf 'COMMAND: cmp %s /candidate/solution.mpy\n' "$generated"
printf 'BYTE_IDENTITY_EXIT_STATUS: %s\n' "$compare_status"
sha256sum "$scratch/solution.py" /candidate/solution.mpy "$generated"
exit "$compare_status"
