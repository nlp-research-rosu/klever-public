#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/k_inventory.py\n'
python3 /audit-output/evidence/k_inventory.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
