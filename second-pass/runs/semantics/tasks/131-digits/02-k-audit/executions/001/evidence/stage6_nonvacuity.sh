#!/usr/bin/env bash
set -u

WORK_DIR=/tmp/audit-work/audit-131-digits
CANDIDATE_DIR="$WORK_DIR/candidate"
MUTATION="$CANDIDATE_DIR/spec-vacuity-audit.k"
PRESERVED_MUTATION=/audit-output/evidence/spec-vacuity-audit.k
LOG_FILE=/audit-output/evidence/stage6_nonvacuity.log
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

run cp "$MUTATION" "$PRESERVED_MUTATION"
run diff -u "$CANDIDATE_DIR/spec.k" "$MUTATION"
run python3 /audit-output/evidence/adequacy_witness.py
run timeout 180 kprove \
  "$MUTATION" \
  --definition "$WORK_DIR/verification-kompiled" \
  --spec-module DIGITS-SPEC-AUDIT-VACUITY \
  --dry-run
run timeout 600 kprove \
  "$MUTATION" \
  --definition "$WORK_DIR/verification-kompiled" \
  --spec-module DIGITS-SPEC-AUDIT-VACUITY
