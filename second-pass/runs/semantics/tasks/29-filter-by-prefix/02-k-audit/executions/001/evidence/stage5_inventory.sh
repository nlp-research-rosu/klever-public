#!/usr/bin/env bash
set -u

status=0

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/inventory_k.py > /audit-output/evidence/rule_inventory.md'
python3 /audit-output/evidence/inventory_k.py \
  > /audit-output/evidence/rule_inventory.md
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: wc -l /audit-output/evidence/rule_inventory.md'
wc -l /audit-output/evidence/rule_inventory.md
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: rg -n "function|functional|total|simplification|priority|owise|macro|trusted" /audit-output/evidence/rule_inventory.md'
rg -n "function|functional|total|simplification|priority|owise|macro|trusted" \
  /audit-output/evidence/rule_inventory.md
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
