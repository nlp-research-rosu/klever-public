#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/31-is-prime
regenerated="$scratch/solution.regenerated.mpy"

printf 'TRANSLATE_COMMAND: python3 %q %q\n' \
  "$scratch/py2mpy.py" "$scratch/solution.py"
python3 "$scratch/py2mpy.py" "$scratch/solution.py" > "$regenerated"
translate_status=$?
printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"

printf 'COMPARE_COMMAND: cmp -- %q %q\n' \
  "$regenerated" "$scratch/solution.mpy"
cmp -- "$regenerated" "$scratch/solution.mpy"
compare_status=$?
printf 'COMPARE_EXIT_STATUS: %d\n' "$compare_status"

sha256sum "$scratch/solution.py" "$scratch/solution.mpy" "$regenerated"
exit "$compare_status"
