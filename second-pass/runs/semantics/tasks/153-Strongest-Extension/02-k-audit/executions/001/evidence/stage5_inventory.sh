#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/k_rule_inventory.py > /audit-output/evidence/k_rule_inventory.md\n'
python3 /audit-output/evidence/k_rule_inventory.py \
  > /audit-output/evidence/k_rule_inventory.md
status=$?
printf '[exit %d]\n' "$status"

printf '$ wc -l /audit-output/evidence/k_rule_inventory.md\n'
wc -l /audit-output/evidence/k_rule_inventory.md
status=$?
printf '[exit %d]\n' "$status"

printf '$ sha256sum /audit-output/evidence/k_rule_inventory.md\n'
sha256sum /audit-output/evidence/k_rule_inventory.md
status=$?
printf '[exit %d]\n' "$status"

printf '$ sed -n 1,70p /audit-output/evidence/k_rule_inventory.md\n'
sed -n '1,70p' /audit-output/evidence/k_rule_inventory.md
status=$?
printf '[exit %d]\n' "$status"
