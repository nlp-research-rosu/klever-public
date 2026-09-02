#!/usr/bin/env bash
set -uo pipefail

trusted_translator=/reference/py2mpy.py
submitted_python=/tmp/audit-work/src/solution.py
regenerated_mpy=/tmp/audit-work/build/solution.regenerated.mpy
submitted_mpy=/tmp/audit-work/src/solution.mpy

printf 'COMMAND: python3 %q %q > %q\n' \
  "$trusted_translator" "$submitted_python" "$regenerated_mpy"
python3 "$trusted_translator" "$submitted_python" > "$regenerated_mpy"
translate_status=$?
printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

printf 'COMMAND: cmp %q %q\n' "$regenerated_mpy" "$submitted_mpy"
cmp "$regenerated_mpy" "$submitted_mpy"
compare_status=$?
printf 'CMP_EXIT_STATUS: %d\n' "$compare_status"

printf 'COMMAND: sha256sum %q %q\n' "$regenerated_mpy" "$submitted_mpy"
sha256sum "$regenerated_mpy" "$submitted_mpy"
exit "$compare_status"
