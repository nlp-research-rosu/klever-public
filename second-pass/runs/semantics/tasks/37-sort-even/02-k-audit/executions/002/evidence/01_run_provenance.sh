#!/usr/bin/env bash
set -u

log="/audit-output/evidence/01-provenance.log"
printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/provenance_audit.py' \
  > "$log"
python3 /audit-output/evidence/provenance_audit.py >> "$log" 2>&1
status=$?
printf 'EXIT_STATUS: %s\n' "$status" >> "$log"
exit "$status"
