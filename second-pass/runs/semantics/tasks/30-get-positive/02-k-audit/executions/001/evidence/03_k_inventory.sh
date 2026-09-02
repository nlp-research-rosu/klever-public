#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/03_k_inventory.py > /audit-output/evidence/RULE-INVENTORY.md\n'
python3 /audit-output/evidence/03_k_inventory.py \
  > /audit-output/evidence/RULE-INVENTORY.md
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
