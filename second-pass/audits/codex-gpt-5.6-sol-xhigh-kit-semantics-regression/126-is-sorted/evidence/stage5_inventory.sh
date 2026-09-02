#!/usr/bin/env bash
set -uo pipefail
set -x

python3 /audit-output/evidence/k_inventory.py \
  > /audit-output/evidence/k_rule_inventory.txt
status=$?
printf 'inventory_generator_status=%s\n' "$status"

sed -n '1,120p' /audit-output/evidence/k_rule_inventory.txt
printf '%s\n' 'INVENTORY TAIL'
tail -n 40 /audit-output/evidence/k_rule_inventory.txt

exit "$status"
