#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 check-integrity.py'
python3 /audit-output/evidence/stage1/check-integrity.py
status=$?
echo "exit_status=$status"
exit "$status"
