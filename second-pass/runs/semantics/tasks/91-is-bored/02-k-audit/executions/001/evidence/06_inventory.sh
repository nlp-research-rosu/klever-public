#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/rule_inventory.py > /audit-output/evidence/rule_inventory.tsv\n'
python3 /audit-output/evidence/rule_inventory.py > /audit-output/evidence/rule_inventory.tsv
status=$?
printf '[exit %d]\n' "$status"

if (( status == 0 )); then
  printf '$ wc -l -c /audit-output/evidence/rule_inventory.tsv\n'
  wc -l -c /audit-output/evidence/rule_inventory.tsv
  status=$?
  printf '[exit %d]\n' "$status"
fi

printf '\nInventory summary:\n'
sed -n '1,40p' /audit-output/evidence/rule_inventory.tsv
exit "$status"
