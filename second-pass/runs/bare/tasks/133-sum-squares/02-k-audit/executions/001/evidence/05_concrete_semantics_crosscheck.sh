#!/usr/bin/env bash
set -u

log=/audit-output/evidence/05_concrete_semantics_crosscheck.log
exec > >(tee "$log") 2>&1

printf 'COMMAND: python3 /audit-output/evidence/05_concrete_semantics_crosscheck.py\n'
python3 /audit-output/evidence/05_concrete_semantics_crosscheck.py
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
