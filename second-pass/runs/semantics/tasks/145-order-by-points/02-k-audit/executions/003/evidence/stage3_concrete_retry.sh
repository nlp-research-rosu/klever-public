#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

printf '%s\n' 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/source/reviewer_concrete.py > /tmp/audit-work/source/reviewer_concrete.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/source/reviewer_concrete.py \
  > /tmp/audit-work/source/reviewer_concrete.mpy
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: krun /tmp/audit-work/source/reviewer_concrete.mpy --definition /tmp/audit-work/source/runtime-kompiled'
krun \
  /tmp/audit-work/source/reviewer_concrete.mpy \
  --definition /tmp/audit-work/source/runtime-kompiled
printf 'EXIT_STATUS: %s\n' "$?"
