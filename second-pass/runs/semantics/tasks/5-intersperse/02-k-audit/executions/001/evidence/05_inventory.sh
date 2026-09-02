#!/usr/bin/env bash
set +e

printf '%s\n' '$ python3 /audit-output/evidence/05_inventory.py > /audit-output/evidence/05_rule_inventory.md'
python3 /audit-output/evidence/05_inventory.py \
  > /audit-output/evidence/05_rule_inventory.md
printf '[exit %d]\n' "$?"

printf '%s\n' '$ wc -l -c /audit-output/evidence/05_rule_inventory.md'
wc -l -c /audit-output/evidence/05_rule_inventory.md
printf '[exit %d]\n' "$?"

printf '%s\n' '$ rg -n \"^\\s*(configuration|syntax|rule|claim|context)\\b\" /tmp/audit-work/candidate/reference-semantics /tmp/audit-work/candidate/verification.k | wc -l'
rg -n '^\s*(configuration|syntax|rule|claim|context)\b' \
  /tmp/audit-work/candidate/reference-semantics \
  /tmp/audit-work/candidate/verification.k | wc -l
printf '[exit %d]\n' "$?"
