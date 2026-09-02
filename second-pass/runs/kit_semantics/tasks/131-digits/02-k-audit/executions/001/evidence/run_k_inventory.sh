#!/usr/bin/env bash
set -o pipefail

echo '$ python3 /audit-output/evidence/k_inventory.py'
python3 /audit-output/evidence/k_inventory.py
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
