#!/usr/bin/env bash
set -u

log=/audit-output/evidence/01_trace_summary.log
exec > >(tee "$log") 2>&1

printf 'COMMAND: python3 /audit-output/evidence/01_trace_summary.py\n'
python3 /audit-output/evidence/01_trace_summary.py
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
