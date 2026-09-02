#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/05_inventory.py'
python3 /audit-output/evidence/05_inventory.py
status=$?
printf 'INVENTORY_EXIT=%s\n' "$status"
exit "$status"
