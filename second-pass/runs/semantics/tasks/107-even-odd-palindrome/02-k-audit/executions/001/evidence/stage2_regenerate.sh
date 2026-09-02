#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 99

python3 /reference/py2mpy.py solution.py \
  > /audit-output/evidence/regenerated-solution.mpy
translate_status=$?

cmp --silent /audit-output/evidence/regenerated-solution.mpy solution.mpy
cmp_status=$?

sha256sum \
  /reference/py2mpy.py \
  solution.py \
  solution.mpy \
  /audit-output/evidence/regenerated-solution.mpy

printf 'translator_exit=%s\ncmp_exit=%s\n' \
  "$translate_status" "$cmp_status"

if (( translate_status != 0 || cmp_status != 0 )); then
  exit 1
fi
