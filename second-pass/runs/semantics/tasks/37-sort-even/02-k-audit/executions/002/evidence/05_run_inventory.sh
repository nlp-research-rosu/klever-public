#!/usr/bin/env bash
set -u

python3 /audit-output/evidence/rule_inventory.py
status=$?
printf 'RUNNER_EXIT_STATUS: %s\n' "$status" >> /audit-output/evidence/05-rule-inventory-summary.log
exit "$status"
