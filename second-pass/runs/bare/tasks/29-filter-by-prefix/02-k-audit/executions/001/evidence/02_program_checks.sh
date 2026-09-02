#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 trusted/py2mpy.py candidate/solution.py > generated/solution.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/generated/solution.mpy
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

printf '%s\n' 'COMMAND: sha256sum submitted and independently regenerated solution.mpy'
sha256sum \
  /tmp/audit-work/candidate/solution.mpy \
  /tmp/audit-work/generated/solution.mpy
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: cmp -s candidate/solution.mpy generated/solution.mpy'
cmp -s \
  /tmp/audit-work/candidate/solution.mpy \
  /tmp/audit-work/generated/solution.mpy
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
status=$?
printf 'EXIT: %s\n' "$status"
exit "$status"
