#!/usr/bin/env bash
set -u -o pipefail

printf '$ python3 /audit-output/evidence/integrity_check.py\n'
python3 /audit-output/evidence/integrity_check.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
