#!/usr/bin/env bash
set -uo pipefail
set -x

status=0

python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/solution.regenerated.mpy
rc=$?
printf 'trusted_translation_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

cmp -s /tmp/audit-work/solution.regenerated.mpy /candidate/solution.mpy
rc=$?
printf 'solution_mpy_byte_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

sha256sum \
  /tmp/audit-work/solution.regenerated.mpy \
  /candidate/solution.mpy \
  /candidate/solution.py \
  /reference/canonical.py

python3 /audit-output/evidence/differential_test.py
rc=$?
printf 'differential_test_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf 'stage2_fidelity_exit=%d\n' "$status"
exit "$status"
