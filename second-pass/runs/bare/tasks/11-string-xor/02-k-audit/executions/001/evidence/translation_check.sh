#!/usr/bin/env bash
set -uo pipefail

python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
translate_status=$?
echo "translator exit: $translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

cmp -s solution.regenerated.mpy solution.mpy
cmp_status=$?
echo "byte comparison exit: $cmp_status"
sha256sum solution.py solution.mpy solution.regenerated.mpy \
          /reference/py2mpy.py
if (( cmp_status != 0 )); then
  diff -u solution.mpy solution.regenerated.mpy
fi
exit "$cmp_status"
