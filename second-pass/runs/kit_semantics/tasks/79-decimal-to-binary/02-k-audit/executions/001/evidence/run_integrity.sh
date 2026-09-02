#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/check_integrity.py'
python3 /audit-output/evidence/check_integrity.py
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
