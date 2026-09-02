#!/usr/bin/env bash
set -uo pipefail

inventory=/audit-output/evidence/04_rule_inventory.txt

echo "COMMAND python3 /audit-output/evidence/04_rule_inventory.py > $inventory"
python3 /audit-output/evidence/04_rule_inventory.py > "$inventory"
inventory_status=$?
echo "INVENTORY_EXIT=$inventory_status"

echo "COMMAND sha256sum $inventory"
sha256sum "$inventory"
hash_status=$?
echo "SHA256_EXIT=$hash_status"

echo "COMMAND sed -n '1,/PER_FILE_END/p' $inventory"
sed -n '1,/PER_FILE_END/p' "$inventory"
summary_status=$?
echo "SUMMARY_READ_EXIT=$summary_status"

if [[ $inventory_status -eq 0 && $hash_status -eq 0 && $summary_status -eq 0 ]]; then
  exit 0
fi
exit 1
