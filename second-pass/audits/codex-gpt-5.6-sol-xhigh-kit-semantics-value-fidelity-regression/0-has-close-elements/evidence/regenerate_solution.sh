#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/reconstruction

printf '%s\n' \
  'COMMAND: python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy'
python3 /reference/py2mpy.py \
  "$work/solution.py" >"$work/solution.regenerated.mpy"
translator_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %s\n' "$translator_status"

printf '%s\n' \
  'COMMAND: cmp /tmp/audit-work/reconstruction/solution.regenerated.mpy /tmp/audit-work/reconstruction/solution.mpy'
cmp "$work/solution.regenerated.mpy" "$work/solution.mpy"
cmp_status=$?
printf 'CMP_EXIT_STATUS: %s\n' "$cmp_status"

sha256sum "$work/solution.py" "$work/solution.mpy" "$work/solution.regenerated.mpy"
printf '%s\n' 'RESULT: submitted solution.mpy is byte-identical to trusted regeneration'
