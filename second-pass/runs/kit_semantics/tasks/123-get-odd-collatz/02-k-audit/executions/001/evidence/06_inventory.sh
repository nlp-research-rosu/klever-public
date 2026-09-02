#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

python3 /audit-output/evidence/06_k_inventory.py \
  > /audit-output/evidence/06_rule_inventory.txt
printf 'inventory_exit=%s\n' "$?"

rg -n \
  '(\[(function|total|functional|simplification|concrete|owise|priority|no-evaluators)|syntax|configuration|context|rule|claim)' \
  /tmp/audit-work/candidate/reference-semantics \
  /tmp/audit-work/candidate/verification.k \
  /tmp/audit-work/candidate/spec.k \
  > /audit-output/evidence/06_rg_inventory.txt
printf 'independent_rg_inventory_exit=%s\n' "$?"

wc -lc \
  /audit-output/evidence/06_rule_inventory.txt \
  /audit-output/evidence/06_rg_inventory.txt
sha256sum \
  /audit-output/evidence/06_rule_inventory.txt \
  /audit-output/evidence/06_rg_inventory.txt
rg '^FILE |^TOTAL_KINDS' /audit-output/evidence/06_rule_inventory.txt
