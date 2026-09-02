#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/02_differential.py\n'
python3 /audit-output/evidence/02_differential.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"

