#!/usr/bin/env bash
set -uo pipefail
set -x

python3 /audit-output/evidence/rule_inventory.py \
  > /audit-output/evidence/rule_inventory.md
inventory_exit=$?
printf 'inventory_exit=%s\n' "$inventory_exit"

wc -l /audit-output/evidence/rule_inventory.md
sed -n '1,45p' /audit-output/evidence/rule_inventory.md

printf '%s\n' 'proof_local_attributes'
rg -n \
  '^\s*(syntax|configuration|context|rule|claim)\b|function|total|functional|no-evaluators|priority|simplification|concrete|owise|macro' \
  /tmp/audit-work/reconstruction/verification.k \
  /tmp/audit-work/reconstruction/spec.k
attribute_scan_exit=$?
printf 'proof_local_attribute_scan_exit=%s\n' "$attribute_scan_exit"

if [[ "$inventory_exit" != 0 || "$attribute_scan_exit" != 0 ]]; then
  exit 1
fi
exit 0
