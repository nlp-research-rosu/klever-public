#!/usr/bin/env bash
set +e

echo '$ python3 /audit-output/evidence/rule_inventory.py'
python3 /audit-output/evidence/rule_inventory.py \
  > /audit-output/evidence/rule_inventory.txt
status=$?
echo "exit=$status"
wc -l /audit-output/evidence/rule_inventory.txt
sha256sum /audit-output/evidence/rule_inventory.txt
exit "$status"
