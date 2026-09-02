#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/03_semantics_compare.py'
python3 /audit-output/evidence/03_semantics_compare.py
status=$?
printf '[exit_status=%d]\n' "$status"
exit "$status"
