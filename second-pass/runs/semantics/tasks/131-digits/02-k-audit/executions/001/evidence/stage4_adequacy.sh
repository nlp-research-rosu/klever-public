#!/usr/bin/env bash
set -u

WORK_DIR=/tmp/audit-work/audit-131-digits
LOG_FILE=/audit-output/evidence/stage4_adequacy.log
: > "$LOG_FILE"

run() {
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } >> "$LOG_FILE"
  "$@" >> "$LOG_FILE" 2>&1
  status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status" >> "$LOG_FILE"
  return 0
}

run krun \
  "$WORK_DIR/candidate/solution.mpy" \
  --definition "$WORK_DIR/concrete-kompiled" \
  --output pretty
run python3 /audit-output/evidence/adequacy_witness.py
run sha256sum \
  "$WORK_DIR/candidate/solution.mpy" \
  "$WORK_DIR/regenerated-solution.mpy" \
  "$WORK_DIR/candidate/spec.k"
