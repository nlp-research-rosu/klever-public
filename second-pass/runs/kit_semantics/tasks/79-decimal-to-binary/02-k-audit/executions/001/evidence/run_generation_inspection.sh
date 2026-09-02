#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/inspect_generation.py'
python3 /audit-output/evidence/inspect_generation.py
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
