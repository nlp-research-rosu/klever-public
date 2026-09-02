#!/usr/bin/env bash
set -u

log="/audit-output/evidence/provenance.log"
python3 /audit-output/evidence/provenance_check.py >"${log}" 2>&1
status=$?
printf '\nCOMMAND: python3 /audit-output/evidence/provenance_check.py\n' >>"${log}"
printf 'EXIT_STATUS: %s\n' "${status}" >>"${log}"
exit "${status}"
