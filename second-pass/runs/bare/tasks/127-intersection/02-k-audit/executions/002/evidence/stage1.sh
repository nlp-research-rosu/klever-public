#!/usr/bin/env bash
set -u

echo 'COMMAND: python3 /audit-output/evidence/integrity_check.py'
python3 /audit-output/evidence/integrity_check.py
status=$?
echo "EXIT: ${status}"
exit "${status}"
