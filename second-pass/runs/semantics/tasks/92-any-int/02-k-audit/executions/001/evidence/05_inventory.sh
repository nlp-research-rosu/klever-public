#!/usr/bin/env bash
set -u

echo '$ python3 /audit-output/evidence/05_inventory.py'
python3 /audit-output/evidence/05_inventory.py
status=$?
echo "exit=$status"

if test "$status" -eq 0; then
  echo '$ sha256sum /audit-output/evidence/05_rule_inventory.md'
  sha256sum /audit-output/evidence/05_rule_inventory.md
  echo '$ wc -l -c /audit-output/evidence/05_rule_inventory.md'
  wc -l -c /audit-output/evidence/05_rule_inventory.md
fi
exit "$status"
