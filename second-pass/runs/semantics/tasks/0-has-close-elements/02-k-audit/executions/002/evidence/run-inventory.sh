#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/05-rule-inventory.log
exec > >(tee "$LOG") 2>&1

echo '$ python3 /audit-output/evidence/inventory_k.py'
python3 /audit-output/evidence/inventory_k.py
echo "[exit $?]"
echo '$ wc -l inventory artifacts'
wc -l \
  /audit-output/evidence/05-rule-inventory.tsv \
  /audit-output/evidence/05-rule-inventory-summary.txt
echo "[exit $?]"
echo '$ SHA-256 inventory artifacts'
sha256sum \
  /audit-output/evidence/inventory_k.py \
  /audit-output/evidence/05-rule-inventory.tsv \
  /audit-output/evidence/05-rule-inventory-summary.txt
echo "[exit $?]"
