#!/usr/bin/env bash
set -uo pipefail

python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translate_status=$?
printf 'translator_exit=%s\n' "$translate_status"
sha256sum solution.mpy solution.regenerated.mpy
cmp -s solution.mpy solution.regenerated.mpy
cmp_status=$?
printf 'byte_identity_cmp_exit=%s\n' "$cmp_status"

if [[ $translate_status -ne 0 || $cmp_status -ne 0 ]]; then
  exit 1
fi
