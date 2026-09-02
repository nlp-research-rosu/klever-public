#!/usr/bin/env bash
set -u

echo 'COMMAND: python3 /audit-output/evidence/05_inventory.py'
python3 /audit-output/evidence/05_inventory.py
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: list every proof-local inventory row'
awk -F '\t' 'NR == 1 || index($1, "/verification.k") || index($1, "/spec.k")' \
  /audit-output/evidence/05_rule_inventory.tsv
status=$?
echo "EXIT_STATUS: $status"
exit "$status"
