#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
status=$?
printf '[exit_status=%d]\n' "$status"
exit "$status"
