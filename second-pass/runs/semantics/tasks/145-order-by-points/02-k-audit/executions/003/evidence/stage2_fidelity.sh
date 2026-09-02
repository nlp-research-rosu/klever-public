#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/source/solution.regenerated.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/source/solution.regenerated.mpy
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: cmp -s /tmp/audit-work/source/solution.regenerated.mpy /tmp/audit-work/source/solution.mpy'
cmp -s \
  /tmp/audit-work/source/solution.regenerated.mpy \
  /tmp/audit-work/source/solution.mpy
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: sha256sum submitted and regenerated solution.mpy'
sha256sum \
  /tmp/audit-work/source/solution.mpy \
  /tmp/audit-work/source/solution.regenerated.mpy
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
printf 'EXIT_STATUS: %s\n' "$?"
