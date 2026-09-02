#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/05_summary_math.py\n'
python3 /audit-output/evidence/05_summary_math.py
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
