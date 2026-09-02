#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/whitespace_check.py'
python3 /audit-output/evidence/whitespace_check.py
code=$?
printf 'EXIT: %s\n' "$code"
exit "$code"
