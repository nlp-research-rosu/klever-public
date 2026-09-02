#!/usr/bin/env bash
set -uo pipefail

echo "$ python3 /audit-output/evidence/rule_inventory.py"
python3 /audit-output/evidence/rule_inventory.py
command_status=$?
echo "EXIT: $command_status"
exit "$command_status"
