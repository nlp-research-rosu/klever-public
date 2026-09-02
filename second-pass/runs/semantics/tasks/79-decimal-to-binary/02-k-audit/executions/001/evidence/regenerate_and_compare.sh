#!/usr/bin/env bash
set -u

work=/tmp/audit-work/79-decimal-to-binary
generated=$work/solution.regenerated.mpy

python3 "$work/trusted-py2mpy.py" "$work/solution.py" > "$generated"
translate_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translate_status"
if [ "$translate_status" -ne 0 ]; then
  exit "$translate_status"
fi

cmp "$generated" "$work/solution.mpy"
cmp_status=$?
printf 'BYTE_IDENTITY_CMP_STATUS: %d\n' "$cmp_status"
if [ "$cmp_status" -ne 0 ]; then
  diff -u "$work/solution.mpy" "$generated"
fi
exit "$cmp_status"
