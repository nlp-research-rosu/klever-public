#!/usr/bin/env bash
set -u

python3 py2mpy.py solution.py > regenerated-solution.mpy
translate_status=$?
printf 'translate_exit=%s\n' "$translate_status"

cmp -s regenerated-solution.mpy solution.mpy
cmp_status=$?
printf 'byte_identity_exit=%s\n' "$cmp_status"

sha256sum solution.py solution.mpy regenerated-solution.mpy py2mpy.py

if [[ "$translate_status" -ne 0 || "$cmp_status" -ne 0 ]]; then
  exit 1
fi
