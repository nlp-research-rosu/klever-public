#!/usr/bin/env bash
set -u

printf '%s\n' '$ python3 /audit-output/evidence/program_pinning.py'
python3 /audit-output/evidence/program_pinning.py
status=$?
printf 'EXIT: %s\n' "$status"
exit "$status"
