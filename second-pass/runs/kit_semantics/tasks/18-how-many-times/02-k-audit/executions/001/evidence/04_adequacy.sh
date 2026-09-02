#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/04_pinning_check.py'
python3 /audit-output/evidence/04_pinning_check.py
pin_status=$?
printf 'PINNING_SCRIPT_EXIT=%s\n' "$pin_status"

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/04_claim_witnesses.py'
python3 /audit-output/evidence/04_claim_witnesses.py
witness_status=$?
printf 'WITNESS_SCRIPT_EXIT=%s\n' "$witness_status"

if [ "$pin_status" -ne 0 ] || [ "$witness_status" -ne 0 ]; then
  exit 1
fi
