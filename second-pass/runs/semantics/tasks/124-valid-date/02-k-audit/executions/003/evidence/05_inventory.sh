#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/05_inventory.log

{
  printf '%s\n' 'COMMAND: python3 /audit-output/evidence/05_inventory.py'
  python3 /audit-output/evidence/05_inventory.py
  STATUS=$?
  printf 'EXIT_STATUS: %s\n' "$STATUS"

  printf '%s\n' 'COMMAND: rg candidate extension classes'
  rg -n \
    '(^|[[:space:]])(syntax|rule|claim|context|configuration)|function|total|functional|no-evaluators|priority|simplification|concrete|owise' \
    /tmp/audit-work/124-valid-date/verification.k \
    /tmp/audit-work/124-valid-date/spec.k
  printf 'EXIT_STATUS: %s\n' "$?"
} >"$LOG" 2>&1

sed -n '1,320p' "$LOG"
