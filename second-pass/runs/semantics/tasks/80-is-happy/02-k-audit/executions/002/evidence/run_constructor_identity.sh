#!/usr/bin/env bash
set -u

log="/audit-output/evidence/constructor-identity.log"
printf 'COMMAND: python3 /audit-output/evidence/constructor_identity.py\n' >"${log}"
python3 /audit-output/evidence/constructor_identity.py >>"${log}" 2>&1
status=$?
printf 'EXIT_STATUS: %s\n' "${status}" >>"${log}"
exit "${status}"
