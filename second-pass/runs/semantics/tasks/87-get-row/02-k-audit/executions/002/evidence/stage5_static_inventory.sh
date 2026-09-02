#!/usr/bin/env bash
set -uo pipefail
set -x

python3 /audit-output/evidence/rule_inventory.py \
  > /audit-output/evidence/rule_inventory.tsv
rc=$?
printf 'inventory_generation_exit=%d\n' "$rc"

wc -l -c /audit-output/evidence/rule_inventory.tsv
sed -n '1,45p' /audit-output/evidence/rule_inventory.tsv
rg -n \
  'opaque/no-evaluators|priority|simplification|functional|/candidate/verification.k|/candidate/spec.k' \
  /audit-output/evidence/rule_inventory.tsv
rg_rc=$?
printf 'inventory_selected_review_exit=%d\n' "$rg_rc"

test "$rc" -eq 0
exit $?
