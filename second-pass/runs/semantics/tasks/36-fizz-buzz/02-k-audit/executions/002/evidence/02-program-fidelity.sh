#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/02-program-fidelity.log
: > "$LOG"

run() {
  printf '$ %s\n' "$*" >> "$LOG"
  "$@" >> "$LOG" 2>&1
  status=$?
  printf 'EXIT: %s\n\n' "$status" >> "$LOG"
  return 0
}

run sha256sum \
  /tmp/audit-work/reviewer-002/scratch/canonical.py \
  /tmp/audit-work/reviewer-002/scratch/solution.py \
  /tmp/audit-work/reviewer-002/scratch/solution.mpy \
  /tmp/audit-work/reviewer-002/scratch/py2mpy.py

printf '%s\n' \
  '$ python3 py2mpy.py solution.py > regenerated-solution.mpy' \
  >> "$LOG"
(
  cd /tmp/audit-work/reviewer-002/scratch || exit 125
  python3 py2mpy.py solution.py > regenerated-solution.mpy
) >> "$LOG" 2>&1
status=$?
printf 'EXIT: %s\n\n' "$status" >> "$LOG"

run cmp -l \
  /tmp/audit-work/reviewer-002/scratch/solution.mpy \
  /tmp/audit-work/reviewer-002/scratch/regenerated-solution.mpy
run sha256sum \
  /tmp/audit-work/reviewer-002/scratch/solution.mpy \
  /tmp/audit-work/reviewer-002/scratch/regenerated-solution.mpy
run python3 /audit-output/evidence/differential_test.py
