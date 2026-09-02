#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/static_review.py'
python3 /audit-output/evidence/static_review.py
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
