#!/usr/bin/env bash
set -u
set -o pipefail
set -x

python3 /reference/py2mpy.py /tmp/audit-work/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
translator_exit=$?
cmp /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/solution.mpy
cmp_exit=$?
sha256sum /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/solution.mpy
python3 /audit-output/evidence/stage2_differential.py
differential_exit=$?
printf 'translator_exit=%s\ncmp_exit=%s\ndifferential_exit=%s\n' \
  "$translator_exit" "$cmp_exit" "$differential_exit"
if (( translator_exit != 0 || cmp_exit != 0 || differential_exit != 0 )); then
  exit 1
fi
printf 'SCRIPT_EXIT=0\n'
