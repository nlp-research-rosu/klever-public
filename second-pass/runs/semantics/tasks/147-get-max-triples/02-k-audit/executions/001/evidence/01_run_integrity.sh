#!/usr/bin/env bash
set -u

echo 'COMMAND: python3 /audit-output/evidence/01_integrity.py'
python3 /audit-output/evidence/01_integrity.py
status=$?
echo "EXIT_STATUS: $status"
exit "$status"
