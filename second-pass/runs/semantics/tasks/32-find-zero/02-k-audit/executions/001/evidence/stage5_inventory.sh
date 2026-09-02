#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 /audit-output/evidence/rule_inventory.py > /audit-output/evidence/rule_inventory.txt\n'
python3 /audit-output/evidence/rule_inventory.py > /audit-output/evidence/rule_inventory.txt
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '\nCOMMAND: wc -l -c /audit-output/evidence/rule_inventory.txt\n'
wc -l -c /audit-output/evidence/rule_inventory.txt
printf 'EXIT_STATUS: %d\n' "$?"

printf '\nCOMMAND: rg -n \"^TOTALS |verification.k\" /audit-output/evidence/rule_inventory.txt\n'
rg -n '^TOTALS |verification\.k' /audit-output/evidence/rule_inventory.txt
printf 'EXIT_STATUS: %d\n' "$?"
