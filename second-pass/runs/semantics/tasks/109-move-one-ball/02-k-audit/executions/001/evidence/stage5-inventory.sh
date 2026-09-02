#!/usr/bin/env bash
set +e

printf '$ python3 /audit-output/evidence/inventory-k.py > /audit-output/evidence/k-rule-inventory.md\n'
python3 /audit-output/evidence/inventory-k.py > /audit-output/evidence/k-rule-inventory.md
status=$?
printf '[exit %d]\n' "$status"
printf '$ sha256sum /audit-output/evidence/k-rule-inventory.md\n'
sha256sum /audit-output/evidence/k-rule-inventory.md
hash_status=$?
printf '[exit %d]\n' "$hash_status"
exit "$status"
