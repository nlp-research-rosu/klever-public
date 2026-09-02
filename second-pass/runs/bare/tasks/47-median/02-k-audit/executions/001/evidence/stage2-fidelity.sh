#!/usr/bin/env bash
set +e

record() {
  printf '$ %s\n' "$*"
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return 0
}

record python3 /tmp/audit-work/47-median/trusted/py2mpy.py \
  /tmp/audit-work/47-median/candidate-src/solution.py

printf '$ trusted translation to /tmp/audit-work/47-median/regenerated-solution.mpy\n'
python3 /tmp/audit-work/47-median/trusted/py2mpy.py \
  /tmp/audit-work/47-median/candidate-src/solution.py \
  > /tmp/audit-work/47-median/regenerated-solution.mpy
printf 'EXIT: %d\n' "$?"

record cmp \
  /tmp/audit-work/47-median/regenerated-solution.mpy \
  /tmp/audit-work/47-median/candidate-src/solution.mpy
record sha256sum \
  /tmp/audit-work/47-median/regenerated-solution.mpy \
  /tmp/audit-work/47-median/candidate-src/solution.mpy
record python3 /audit-output/evidence/differential.py
