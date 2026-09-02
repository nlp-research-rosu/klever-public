#!/usr/bin/env bash
set -o pipefail

echo '$ python3 /audit-output/evidence/provenance_check.py'
python3 /audit-output/evidence/provenance_check.py
status=${PIPESTATUS[0]}
echo "EXIT_STATUS=$status"
exit "$status"
