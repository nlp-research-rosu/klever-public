#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/build_rule_inventory.py > /audit-output/evidence/RULE_INVENTORY.md'
python3 /audit-output/evidence/build_rule_inventory.py \
  > /audit-output/evidence/RULE_INVENTORY.md
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: wc -l -c /audit-output/evidence/RULE_INVENTORY.md'
wc -l -c /audit-output/evidence/RULE_INVENTORY.md
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: rg Overall counts through EOF'
sed -n '/^## Overall counts/,$p' /audit-output/evidence/RULE_INVENTORY.md
printf 'EXIT_STATUS: %s\n' "$?"
