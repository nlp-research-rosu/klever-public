#!/usr/bin/env bash
set -u

EVIDENCE_DIR=/audit-output/evidence
WORK_DIR=/tmp/audit-work/audit-131-digits
LOG_FILE="$EVIDENCE_DIR/stage2_fidelity.log"

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

run python3 "$WORK_DIR/trusted/py2mpy.py" \
  "$WORK_DIR/candidate/solution.py"

{
  printf 'COMMAND: python3 %q %q > %q\n' \
    "$WORK_DIR/trusted/py2mpy.py" \
    "$WORK_DIR/candidate/solution.py" \
    "$WORK_DIR/regenerated-solution.mpy"
} >> "$LOG_FILE"
python3 "$WORK_DIR/trusted/py2mpy.py" \
  "$WORK_DIR/candidate/solution.py" \
  > "$WORK_DIR/regenerated-solution.mpy" 2>> "$LOG_FILE"
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status" >> "$LOG_FILE"

run cmp -s \
  "$WORK_DIR/regenerated-solution.mpy" \
  "$WORK_DIR/candidate/solution.mpy"
run sha256sum \
  "$WORK_DIR/regenerated-solution.mpy" \
  "$WORK_DIR/candidate/solution.mpy"
run diff -u \
  "$WORK_DIR/candidate/solution.mpy" \
  "$WORK_DIR/regenerated-solution.mpy"
run python3 "$EVIDENCE_DIR/differential_test.py"
