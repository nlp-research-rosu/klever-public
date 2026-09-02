#!/usr/bin/env bash
set -u

printf '$ python3 %q\n' /audit-output/evidence/semantics_differential.py
python3 /audit-output/evidence/semantics_differential.py
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
