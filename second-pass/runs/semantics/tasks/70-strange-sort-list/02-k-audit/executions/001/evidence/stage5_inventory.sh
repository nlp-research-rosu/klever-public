#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/inventory_k_sentences.py > /audit-output/evidence/rule_inventory.tsv\n'
python3 /audit-output/evidence/inventory_k_sentences.py \
  > /audit-output/evidence/rule_inventory.tsv
inventory_status=$?
printf '[exit %d]\n' "$inventory_status"

printf '\n$ wc -l -c /audit-output/evidence/rule_inventory.tsv\n'
wc -l -c /audit-output/evidence/rule_inventory.tsv
printf '[exit %d]\n' "$?"

printf '\nInventory summary:\n'
sed -n '/^SUMMARY$/,$p' /audit-output/evidence/rule_inventory.tsv

printf '\nIndependent source-start count:\n'
printf "$ rg -n '^\\\\s*(configuration|context( alias)?|syntax( (priority|associativity|lexical))?|rule|claim|alias)\\\\b' SOURCES | wc -l\n"
rg -n '^\s*(configuration|context( alias)?|syntax( (priority|associativity|lexical))?|rule|claim|alias)\b' \
  /tmp/audit-work/recon/reference-semantics \
  /tmp/audit-work/recon/verification.k \
  /tmp/audit-work/recon/spec.k | wc -l
printf '[exit %d]\n' "${PIPESTATUS[0]}"

exit "$inventory_status"
