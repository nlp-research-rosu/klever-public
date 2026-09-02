#!/usr/bin/env bash
set -u

python3 py2mpy.py solution.py > solution-regenerated.mpy
translate_status=$?
echo "translator_exit=$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

sha256sum solution.py solution.mpy solution-regenerated.mpy
cmp -l solution.mpy solution-regenerated.mpy
compare_status=$?
if [[ "$compare_status" -eq 0 ]]; then
  echo "byte_identity=true"
else
  echo "byte_identity=false"
fi
echo "cmp_exit=$compare_status"
exit "$compare_status"
