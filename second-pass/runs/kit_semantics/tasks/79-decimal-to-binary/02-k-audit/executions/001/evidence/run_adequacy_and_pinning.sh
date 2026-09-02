#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/adequacy_and_pinning.py'
python3 /audit-output/evidence/adequacy_and_pinning.py
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
