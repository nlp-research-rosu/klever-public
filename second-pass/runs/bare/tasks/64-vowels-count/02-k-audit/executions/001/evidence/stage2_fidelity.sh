#!/usr/bin/env bash
set -u
set -x

python3 /reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/solution.trusted-regenerated.mpy
translator_exit=$?
cmp --silent \
  /tmp/audit-work/candidate-src/solution.mpy \
  /tmp/audit-work/solution.trusted-regenerated.mpy
mpy_cmp_exit=$?
sha256sum \
  /tmp/audit-work/candidate-src/solution.mpy \
  /tmp/audit-work/solution.trusted-regenerated.mpy
python3 /audit-output/evidence/differential.py
differential_exit=$?
printf 'translator_exit=%s\n' "$translator_exit"
printf 'mpy_cmp_exit=%s\n' "$mpy_cmp_exit"
printf 'differential_exit=%s\n' "$differential_exit"
test "$translator_exit" -eq 0
test "$mpy_cmp_exit" -eq 0
test "$differential_exit" -eq 0
