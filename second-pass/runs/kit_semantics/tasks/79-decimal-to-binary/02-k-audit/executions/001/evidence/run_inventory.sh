#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/inventory_k.py > /audit-output/evidence/05-rule-inventory.tsv'
python3 /audit-output/evidence/inventory_k.py \
  > /audit-output/evidence/05-rule-inventory.tsv
inventory_status=$?
echo "INVENTORY_EXIT_STATUS=$inventory_status"

echo '$ wc -l /audit-output/evidence/05-rule-inventory.tsv'
wc -l /audit-output/evidence/05-rule-inventory.tsv
wc_status=$?
echo "WC_EXIT_STATUS=$wc_status"

echo '$ tail -80 /audit-output/evidence/05-rule-inventory.tsv'
tail -80 /audit-output/evidence/05-rule-inventory.tsv
tail_status=$?
echo "TAIL_EXIT_STATUS=$tail_status"

if (( inventory_status || wc_status || tail_status )); then
  exit 1
fi
