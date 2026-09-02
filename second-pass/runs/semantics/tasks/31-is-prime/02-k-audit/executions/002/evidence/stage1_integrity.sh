#!/usr/bin/env bash
set -uo pipefail

echo 'COMMAND: python3 /audit-output/evidence/stage1_check.py'
python3 /audit-output/evidence/stage1_check.py
status=$?
echo "EXIT_STATUS: ${status}"
exit "${status}"
