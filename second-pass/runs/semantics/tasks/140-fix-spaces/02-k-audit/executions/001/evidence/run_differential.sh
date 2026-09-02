#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/differential_test.py\n'
python3 /audit-output/evidence/differential_test.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
