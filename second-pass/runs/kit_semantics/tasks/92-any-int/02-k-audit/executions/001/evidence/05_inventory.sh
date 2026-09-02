#!/usr/bin/env bash
set +e

printf '$ python3 /audit-output/evidence/05_inventory.py > /audit-output/evidence/05_rule_inventory.md\n'
python3 /audit-output/evidence/05_inventory.py > /audit-output/evidence/05_rule_inventory.md
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ rg -c "^-" /audit-output/evidence/05_rule_inventory.md\n'
rg -c '^-' /audit-output/evidence/05_rule_inventory.md
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ sha256sum /audit-output/evidence/05_rule_inventory.md\n'
sha256sum /audit-output/evidence/05_rule_inventory.md
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ sed -n "1,90p" /audit-output/evidence/05_rule_inventory.md\n'
sed -n '1,90p' /audit-output/evidence/05_rule_inventory.md
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

exit 0
