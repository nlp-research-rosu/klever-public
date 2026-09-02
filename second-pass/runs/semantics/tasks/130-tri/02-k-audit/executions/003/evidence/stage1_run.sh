#!/usr/bin/env bash
set -uo pipefail

printf 'COMMAND: python3 /audit-output/evidence/stage1_integrity.py\n'
python3 /audit-output/evidence/stage1_integrity.py
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
