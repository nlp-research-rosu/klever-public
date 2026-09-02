#!/usr/bin/env bash
set -o pipefail
printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
exit "$status"
