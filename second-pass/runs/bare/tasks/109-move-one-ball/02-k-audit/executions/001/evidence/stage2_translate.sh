#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage2_translate.log
exec > >(tee "$log") 2>&1

printf '$ python3 /tmp/audit-work/source/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/source/solution.regenerated.mpy\n'
python3 /tmp/audit-work/source/py2mpy.py \
  /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/source/solution.regenerated.mpy
translate_status=$?
printf 'EXIT_STATUS: %d\n' "$translate_status"

printf '$ cmp -s /tmp/audit-work/source/solution.mpy /tmp/audit-work/source/solution.regenerated.mpy\n'
cmp -s \
  /tmp/audit-work/source/solution.mpy \
  /tmp/audit-work/source/solution.regenerated.mpy
cmp_status=$?
printf 'EXIT_STATUS: %d\n' "$cmp_status"

sha256sum \
  /tmp/audit-work/source/solution.mpy \
  /tmp/audit-work/source/solution.regenerated.mpy

if [[ $translate_status -ne 0 || $cmp_status -ne 0 ]]; then
  exit 1
fi

