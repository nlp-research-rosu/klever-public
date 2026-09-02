#!/usr/bin/env bash
set -uo pipefail

printf 'COMMAND: PYTHONDONTWRITEBYTECODE=1 python3 /audit-output/evidence/provenance_check.py\n'
PYTHONDONTWRITEBYTECODE=1 python3 /audit-output/evidence/provenance_check.py
rc=$?
printf 'EXIT: %d\n' "$rc"
exit "$rc"
