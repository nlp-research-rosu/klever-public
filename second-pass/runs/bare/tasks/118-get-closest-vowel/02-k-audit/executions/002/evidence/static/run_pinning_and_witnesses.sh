#!/usr/bin/env bash
set -uo pipefail

printf 'COMMAND=python3 /audit-output/evidence/static/pinning_check.py\n'
python3 /audit-output/evidence/static/pinning_check.py
pin_status=$?
printf 'PINNING_EXIT_STATUS=%s\n' "$pin_status"

printf 'COMMAND=python3 /audit-output/evidence/static/entry_witnesses.py\n'
python3 /audit-output/evidence/static/entry_witnesses.py
witness_status=$?
printf 'WITNESS_EXIT_STATUS=%s\n' "$witness_status"

if (( pin_status != 0 || witness_status != 0 )); then
  exit 1
fi
exit 0
