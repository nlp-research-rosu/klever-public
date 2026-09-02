#!/usr/bin/env bash
set -o pipefail

echo '$ python3 /audit-output/evidence/program_pinning_check.py'
python3 /audit-output/evidence/program_pinning_check.py
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
