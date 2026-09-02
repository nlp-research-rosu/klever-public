#!/usr/bin/env bash
set -u

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/01_generation_inspect.py'
python3 /audit-output/evidence/01_generation_inspect.py
status=$?
printf 'GENERATION_INSPECTION_EXIT=%s\n' "$status"
exit "$status"
