#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/04_pinning.py\n'
python3 /audit-output/evidence/04_pinning.py
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
