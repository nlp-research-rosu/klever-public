#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/02_differential.log
exec >"$LOG" 2>&1

printf '$ python3 /audit-output/evidence/differential_test.py\n'
python3 /audit-output/evidence/differential_test.py
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
