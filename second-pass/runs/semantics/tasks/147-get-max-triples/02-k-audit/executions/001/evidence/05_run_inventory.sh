#!/usr/bin/env bash
set -u

echo 'COMMAND: python3 /audit-output/evidence/05_rule_inventory.py'
python3 /audit-output/evidence/05_rule_inventory.py
status=$?
echo "EXIT_STATUS: $status"
exit "$status"
