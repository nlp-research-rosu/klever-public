#!/usr/bin/env bash
set -u

printf 'COMMAND: python3 /audit-output/evidence/k_inventory.py\n'
python3 /audit-output/evidence/k_inventory.py
rc=$?
printf '\nEXIT_STATUS: %d\n' "$rc"
exit "$rc"
