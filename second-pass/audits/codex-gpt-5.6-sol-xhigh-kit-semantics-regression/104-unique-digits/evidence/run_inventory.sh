#!/usr/bin/env bash
set -u

echo '$ python3 /audit-output/evidence/inventory_k.py > /audit-output/evidence/05-rule-inventory.tsv'
python3 /audit-output/evidence/inventory_k.py \
  > /audit-output/evidence/05-rule-inventory.tsv
inventory_status=$?
echo "EXIT_STATUS=$inventory_status"

echo '$ wc -l /audit-output/evidence/05-rule-inventory.tsv'
wc -l /audit-output/evidence/05-rule-inventory.tsv
wc_status=$?
echo "EXIT_STATUS=$wc_status"

echo '$ rg -n SUPPLIED_OPAQUE_OR_SYMBOLIC_PRIMITIVE /audit-output/evidence/05-rule-inventory.tsv'
rg -n SUPPLIED_OPAQUE_OR_SYMBOLIC_PRIMITIVE \
  /audit-output/evidence/05-rule-inventory.tsv
opaque_status=$?
echo "EXIT_STATUS=$opaque_status"

if [[ "$inventory_status" -ne 0 || "$wc_status" -ne 0 || "$opaque_status" -ne 0 ]]; then
  exit 1
fi
exit 0
