#!/usr/bin/env bash
set -u

log="/audit-output/evidence/summary-differential.log"
printf 'COMMAND: python3 /audit-output/evidence/summary_differential.py\n' >"${log}"
python3 /audit-output/evidence/summary_differential.py >>"${log}" 2>&1
status=$?
printf 'EXIT_STATUS: %s\n' "${status}" >>"${log}"
exit "${status}"
