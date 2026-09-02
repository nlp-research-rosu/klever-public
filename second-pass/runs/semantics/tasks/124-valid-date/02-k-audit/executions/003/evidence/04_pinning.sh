#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/04_pinning.log

{
  printf '%s\n' 'COMMAND: python3 /audit-output/evidence/04_pinning.py'
  python3 /audit-output/evidence/04_pinning.py
  STATUS=$?
  printf 'EXIT_STATUS: %s\n' "$STATUS"

  printf '%s\n' 'COMMAND: cmp exact submitted and trusted-regenerated solution.mpy'
  cmp -s \
    /tmp/audit-work/124-valid-date/solution.mpy \
    /tmp/audit-work/124-valid-date/regenerated-solution.mpy
  printf 'EXIT_STATUS: %s\n' "$?"
} >"$LOG" 2>&1

sed -n '1,240p' "$LOG"
