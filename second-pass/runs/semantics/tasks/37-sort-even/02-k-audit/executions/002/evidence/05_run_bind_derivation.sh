#!/usr/bin/env bash
set -u

log="/audit-output/evidence/05-bind-derivation.log"
printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/bind_rule_derivation.py' \
  > "$log"
python3 /audit-output/evidence/bind_rule_derivation.py >> "$log" 2>&1
status=$?
printf 'EXIT_STATUS: %s\n' "$status" >> "$log"
exit "$status"
