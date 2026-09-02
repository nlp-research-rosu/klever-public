#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/reconstruction
status=0

python3 py2mpy.py solution.py > solution.mpy
translate_exit=$?
printf 'translator_exit=%s\n' "$translate_exit"
if [[ "$translate_exit" != 0 ]]; then
  status=1
fi

sha256sum solution.py solution.mpy solution.submitted.mpy canonical.py
cmp -s solution.mpy solution.submitted.mpy
mpy_compare=$?
printf 'regenerated_mpy_cmp_exit=%s\n' "$mpy_compare"
if [[ "$mpy_compare" != 0 ]]; then
  diff -u solution.submitted.mpy solution.mpy
  status=1
fi

python3 /audit-output/evidence/differential_audit.py
differential_exit=$?
printf 'differential_exit=%s\n' "$differential_exit"
if [[ "$differential_exit" != 0 ]]; then
  status=1
fi

printf 'stage2_program_fidelity_exit=%s\n' "$status"
exit "$status"
