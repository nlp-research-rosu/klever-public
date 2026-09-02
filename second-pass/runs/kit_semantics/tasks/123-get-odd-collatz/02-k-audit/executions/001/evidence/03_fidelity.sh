#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/candidate/solution.regenerated.mpy
translator_exit=$?
printf 'trusted_translator_exit=%s\n' "$translator_exit"

cmp -s \
  /tmp/audit-work/candidate/solution.regenerated.mpy \
  /candidate/solution.mpy
cmp_exit=$?
printf 'solution_mpy_byte_cmp_exit=%s\n' "$cmp_exit"

sha256sum \
  /tmp/audit-work/candidate/solution.regenerated.mpy \
  /candidate/solution.mpy
printf 'solution_mpy_hash_exit=%s\n' "$?"

diff -u \
  /candidate/solution.mpy \
  /tmp/audit-work/candidate/solution.regenerated.mpy
printf 'solution_mpy_diff_exit=%s\n' "$?"

python3 /audit-output/evidence/03_differential.py
differential_exit=$?
printf 'independent_differential_exit=%s\n' "$differential_exit"

if [[ "$translator_exit" -ne 0 || "$cmp_exit" -ne 0 || "$differential_exit" -ne 0 ]]; then
  exit 1
fi
