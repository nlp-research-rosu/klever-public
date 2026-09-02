#!/usr/bin/env bash
set -u

cd /tmp/audit-work/proof || exit 90

python3 py2mpy.py solution.py > solution.regenerated.mpy
translate_rc=$?
printf 'translator_exit=%s\n' "$translate_rc"
if [[ "$translate_rc" -ne 0 ]]; then
  exit "$translate_rc"
fi

cmp -s solution.regenerated.mpy solution.mpy
cmp_rc=$?
printf 'solution_mpy_byte_identity_cmp_exit=%s\n' "$cmp_rc"
if [[ "$cmp_rc" -ne 0 ]]; then
  diff -u solution.mpy solution.regenerated.mpy
  exit "$cmp_rc"
fi

sha256sum solution.py solution.mpy solution.regenerated.mpy
python3 /audit-output/evidence/stage2_differential.py
