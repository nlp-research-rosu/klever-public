#!/usr/bin/env bash
set -u

log="/audit-output/evidence/04-pinning.log"
printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/constructor_compare.py' \
  > "$log"
python3 /audit-output/evidence/constructor_compare.py >> "$log" 2>&1
constructor_status=$?
printf 'CONSTRUCTOR_COMPARE_EXIT_STATUS: %s\n' "$constructor_status" >> "$log"

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/summary_witnesses.py' \
  >> "$log"
python3 /audit-output/evidence/summary_witnesses.py >> "$log" 2>&1
witness_status=$?
printf 'SUMMARY_WITNESS_EXIT_STATUS: %s\n' "$witness_status" >> "$log"

if [ "$constructor_status" -ne 0 ] || [ "$witness_status" -ne 0 ]; then
  exit 1
fi
exit 0
