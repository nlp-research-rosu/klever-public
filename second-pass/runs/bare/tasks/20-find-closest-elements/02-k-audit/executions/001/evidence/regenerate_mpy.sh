#!/usr/bin/env bash
set -uo pipefail

trusted_translator=/reference/py2mpy.py
scratch_source=/tmp/audit-work/source/solution.py
regenerated=/tmp/audit-work/generated-solution.mpy
submitted=/tmp/audit-work/source/solution.mpy

printf 'COMMAND: python3 %q %q > %q\n' \
  "$trusted_translator" "$scratch_source" "$regenerated"
python3 "$trusted_translator" "$scratch_source" >"$regenerated"
translate_status=$?
printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

printf 'COMMAND: cmp -- %q %q\n' "$regenerated" "$submitted"
cmp -- "$regenerated" "$submitted"
compare_status=$?
printf 'CMP_EXIT_STATUS: %d\n' "$compare_status"
sha256sum "$regenerated" "$submitted"
exit "$compare_status"
