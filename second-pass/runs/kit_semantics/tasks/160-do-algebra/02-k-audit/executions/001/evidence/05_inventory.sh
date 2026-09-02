#!/usr/bin/env bash
set -u

inventory=/audit-output/evidence/05_inventory.txt
echo "COMMAND: python3 /audit-output/evidence/05_inventory.py > $inventory"
python3 /audit-output/evidence/05_inventory.py > "$inventory"
status=$?
echo "INVENTORY_EXIT_STATUS=$status"
if (( status != 0 )); then
  exit "$status"
fi
wc -l -c "$inventory"
sha256sum "$inventory"
head -n 35 "$inventory"
rg '^TOTALS|PROOF_LOCAL|RELEVANT_FIXED_RULE_ZERO' "$inventory" | tail -n 80
