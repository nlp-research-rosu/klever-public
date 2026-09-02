#!/usr/bin/env bash
set -u

cd /tmp/audit-work/proof || exit 1
python3 ./trusted/py2mpy.py ./solution.py > ./solution.regenerated.mpy
translator_status=$?
printf 'translator_exit=%d\n' "$translator_status"
if (( translator_status != 0 )); then
  exit "$translator_status"
fi

cmp -s ./solution.mpy ./solution.regenerated.mpy
cmp_status=$?
printf 'byte_identity_cmp_exit=%d\n' "$cmp_status"
sha256sum ./solution.mpy ./solution.regenerated.mpy
if (( cmp_status != 0 )); then
  diff -u ./solution.mpy ./solution.regenerated.mpy
fi
exit "$cmp_status"
