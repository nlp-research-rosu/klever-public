#!/usr/bin/env bash
set -u

work=/tmp/audit-work/59-largest-prime-factor

printf '%s\n' \
  'COMMAND: python3 trusted/py2mpy.py source/solution.py > regenerated.mpy'
python3 "$work/trusted/py2mpy.py" "$work/source/solution.py" \
  > "$work/regenerated.mpy"
translate_status=$?
printf 'EXIT: %d\n' "$translate_status"

printf '%s\n' \
  'COMMAND: cmp -s source/solution.mpy regenerated.mpy'
cmp -s "$work/source/solution.mpy" "$work/regenerated.mpy"
cmp_status=$?
printf 'EXIT: %d\n' "$cmp_status"
sha256sum "$work/source/solution.mpy" "$work/regenerated.mpy"

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
differential_status=$?
printf 'EXIT: %d\n' "$differential_status"

if (( translate_status != 0 || cmp_status != 0 || differential_status != 0 )); then
  exit 1
fi
