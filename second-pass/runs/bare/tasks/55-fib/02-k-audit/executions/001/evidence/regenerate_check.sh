#!/usr/bin/env bash
set -uo pipefail

trusted_translator=/tmp/audit-work/trusted/py2mpy.py
submitted_python=/tmp/audit-work/src/solution.py
submitted_mpy=/tmp/audit-work/src/solution.mpy
regenerated_mpy=/tmp/audit-work/build/solution.regenerated.mpy

printf 'GENERATION_COMMAND: python3 %q %q > %q\n' \
  "$trusted_translator" "$submitted_python" "$regenerated_mpy"
python3 "$trusted_translator" "$submitted_python" > "$regenerated_mpy"
generation_status=$?
printf 'GENERATION_EXIT_STATUS: %d\n' "$generation_status"
if (( generation_status != 0 )); then
  exit "$generation_status"
fi

sha256sum "$submitted_mpy" "$regenerated_mpy"
printf 'COMPARE_COMMAND: cmp -s %q %q\n' "$regenerated_mpy" "$submitted_mpy"
cmp -s "$regenerated_mpy" "$submitted_mpy"
compare_status=$?
printf 'COMPARE_EXIT_STATUS: %d\n' "$compare_status"
if (( compare_status != 0 )); then
  diff -u "$submitted_mpy" "$regenerated_mpy" || true
fi
exit "$compare_status"
