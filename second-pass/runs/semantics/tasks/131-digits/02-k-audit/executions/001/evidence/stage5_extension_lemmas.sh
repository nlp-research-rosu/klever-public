#!/usr/bin/env bash
set -u

WORK_DIR=/tmp/audit-work/audit-131-digits
LOG_FILE=/audit-output/evidence/stage5_extension_lemmas.log
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

run timeout 600 kompile \
  "$WORK_DIR/verification-base.k" \
  --backend haskell \
  --main-module DIGITS-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK_DIR/verification-base-kompiled"
run timeout 600 kprove \
  "$WORK_DIR/extension-lemmas.k" \
  --definition "$WORK_DIR/verification-base-kompiled" \
  --spec-module EXTENSION-LEMMAS \
  --claims EXTENSION-LEMMAS.even-step-equation
run timeout 600 kprove \
  "$WORK_DIR/extension-lemmas.k" \
  --definition "$WORK_DIR/verification-base-kompiled" \
  --spec-module EXTENSION-LEMMAS \
  --claims EXTENSION-LEMMAS.first-odd-step-equation
run timeout 600 kprove \
  "$WORK_DIR/extension-lemmas.k" \
  --definition "$WORK_DIR/verification-base-kompiled" \
  --spec-module EXTENSION-LEMMAS \
  --claims EXTENSION-LEMMAS.later-odd-step-equation
