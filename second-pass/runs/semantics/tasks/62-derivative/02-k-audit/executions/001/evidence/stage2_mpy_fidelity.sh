#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cd "$scratch" || exit 70

printf '%s\n' 'TRANSLATOR_COMMAND: python3 py2mpy.py solution.py'
python3 py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

sha256sum solution.py solution.mpy regenerated-solution.mpy
cmp --silent solution.mpy regenerated-solution.mpy
cmp_status=$?
printf 'BYTE_IDENTITY_CMP_STATUS: %d\n' "$cmp_status"
if (( cmp_status != 0 )); then
  cmp -l solution.mpy regenerated-solution.mpy | sed -n '1,100p'
fi
exit "$cmp_status"
