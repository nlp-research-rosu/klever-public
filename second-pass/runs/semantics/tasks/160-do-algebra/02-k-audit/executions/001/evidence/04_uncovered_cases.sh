#!/usr/bin/env bash
set +e
LOG=/audit-output/evidence/04_uncovered_cases.log
printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/04_uncovered_cases.py' \
  > "$LOG"
python3 /audit-output/evidence/04_uncovered_cases.py >> "$LOG" 2>&1
status=$?
printf 'EXIT: %d\n' "$status" >> "$LOG"
exit "$status"
