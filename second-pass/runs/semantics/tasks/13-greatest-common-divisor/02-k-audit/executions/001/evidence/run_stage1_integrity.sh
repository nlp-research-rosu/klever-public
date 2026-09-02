#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 /audit-output/evidence/integrity_check.py\n'
python3 /audit-output/evidence/integrity_check.py
status=$?
printf 'EXIT STATUS: %d\n' "$status"
exit "$status"
