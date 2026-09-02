#!/usr/bin/env bash
set -uo pipefail
set -x

python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/build/regenerated-solution.mpy
translator_status=$?

cmp -s \
  /tmp/audit-work/build/regenerated-solution.mpy \
  /tmp/audit-work/candidate/solution.mpy
byte_identity_status=$?

sha256sum \
  /tmp/audit-work/build/regenerated-solution.mpy \
  /tmp/audit-work/candidate/solution.mpy
hash_status=$?

python3 /audit-output/evidence/02_differential.py
differential_status=$?

set +x
printf 'translator_exit=%s\n' "$translator_status"
printf 'solution_mpy_byte_identity_exit=%s\n' "$byte_identity_status"
printf 'sha256sum_exit=%s\n' "$hash_status"
printf 'differential_exit=%s\n' "$differential_status"

if (( translator_status != 0 || byte_identity_status != 0 || hash_status != 0 )); then
  exit 2
fi
exit "$differential_status"
