#!/usr/bin/env bash
set -u

status=0

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/claim_witness_check.py'
python3 /audit-output/evidence/claim_witness_check.py
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
