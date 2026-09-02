#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/122-add-elements || exit 70
printf '%s\n' \
  'COMMAND: python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy'
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translate_status=$?
printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

printf '%s\n' 'COMMAND: cmp -s solution.regenerated.mpy solution.mpy'
cmp -s solution.regenerated.mpy solution.mpy
cmp_status=$?
printf 'CMP_EXIT_STATUS: %d\n' "$cmp_status"
sha256sum solution.py solution.mpy solution.regenerated.mpy
exit "$cmp_status"
