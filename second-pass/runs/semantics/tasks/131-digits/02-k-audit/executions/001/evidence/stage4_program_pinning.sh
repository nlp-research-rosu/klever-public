#!/usr/bin/env bash
set -u

WORK_DIR=/tmp/audit-work/audit-131-digits
LOG_FILE=/audit-output/evidence/stage4_program_pinning.log
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

run timeout 180 kprove \
  "$WORK_DIR/program-pinning.k" \
  --definition "$WORK_DIR/verification-kompiled" \
  --spec-module PROGRAM-PINNING \
  --dry-run
run timeout 600 kprove \
  "$WORK_DIR/program-pinning.k" \
  --definition "$WORK_DIR/verification-kompiled" \
  --spec-module PROGRAM-PINNING
