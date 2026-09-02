#!/usr/bin/env bash
set +e
LOG=/audit-output/evidence/02_differential.log
printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/02_differential.py --canonical /reference/canonical.py --candidate /candidate/solution.py --results /audit-output/evidence/02_differential-results.json' \
  > "$LOG"
python3 /audit-output/evidence/02_differential.py \
  --canonical /reference/canonical.py \
  --candidate /candidate/solution.py \
  --results /audit-output/evidence/02_differential-results.json \
  >> "$LOG" 2>&1
status=$?
printf 'EXIT: %d\n' "$status" >> "$LOG"
exit "$status"
