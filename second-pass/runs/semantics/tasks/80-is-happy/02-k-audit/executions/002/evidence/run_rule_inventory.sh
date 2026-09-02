#!/usr/bin/env bash
set -u

log="/audit-output/evidence/rule-inventory.txt"
printf 'COMMAND: python3 /audit-output/evidence/rule_inventory.py\n' >"${log}"
python3 /audit-output/evidence/rule_inventory.py >>"${log}" 2>&1
status=$?
printf '\nEXIT_STATUS: %s\n' "${status}" >>"${log}"
exit "${status}"
