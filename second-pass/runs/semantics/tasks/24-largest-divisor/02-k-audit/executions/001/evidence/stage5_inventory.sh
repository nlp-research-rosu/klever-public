#!/usr/bin/env bash
set -u

echo '$ python3 /audit-output/evidence/stage5_inventory.py > /audit-output/evidence/stage5_rule_inventory.md'
python3 /audit-output/evidence/stage5_inventory.py \
  > /audit-output/evidence/stage5_rule_inventory.md
inventory_rc=$?
printf '[exit %d]\n\n' "$inventory_rc"

echo '$ wc -l /audit-output/evidence/stage5_rule_inventory.md'
wc -l /audit-output/evidence/stage5_rule_inventory.md
wc_rc=$?
printf '[exit %d]\n\n' "$wc_rc"

echo '$ sha256sum /audit-output/evidence/stage5_rule_inventory.md /audit-output/evidence/stage5_used_path.md'
sha256sum \
  /audit-output/evidence/stage5_rule_inventory.md \
  /audit-output/evidence/stage5_used_path.md
hash_rc=$?
printf '[exit %d]\n\n' "$hash_rc"

if (( inventory_rc != 0 || wc_rc != 0 || hash_rc != 0 )); then
  exit 1
fi
