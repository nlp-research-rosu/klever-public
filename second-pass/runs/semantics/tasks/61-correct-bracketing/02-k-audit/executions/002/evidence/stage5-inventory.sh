#!/usr/bin/env bash
set -u

cd /tmp/audit-work/proof || exit 90

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/k_inventory.py'
python3 /audit-output/evidence/k_inventory.py
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
exit "$status"
