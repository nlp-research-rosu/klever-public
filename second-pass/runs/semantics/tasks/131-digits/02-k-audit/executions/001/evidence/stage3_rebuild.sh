#!/usr/bin/env bash
set -u

EVIDENCE_DIR=/audit-output/evidence
WORK_DIR=/tmp/audit-work/audit-131-digits
CANDIDATE_DIR="$WORK_DIR/candidate"
LOG_FILE="$EVIDENCE_DIR/stage3_rebuild.log"

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

run kompile --version
run kprove --version
run diff -u \
  "$CANDIDATE_DIR/solution.py" \
  <(sed -n '1,10p' "$WORK_DIR/reviewer-concrete-tests.py")

{
  printf 'COMMAND: python3 %q %q > %q\n' \
    "$WORK_DIR/trusted/py2mpy.py" \
    "$WORK_DIR/reviewer-concrete-tests.py" \
    "$WORK_DIR/reviewer-concrete-tests.mpy"
} >> "$LOG_FILE"
python3 "$WORK_DIR/trusted/py2mpy.py" \
  "$WORK_DIR/reviewer-concrete-tests.py" \
  > "$WORK_DIR/reviewer-concrete-tests.mpy" 2>> "$LOG_FILE"
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status" >> "$LOG_FILE"

run python3 "$WORK_DIR/reviewer-concrete-tests.py"
run timeout 600 kompile \
  "$CANDIDATE_DIR/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK_DIR/concrete-kompiled"
run timeout 180 krun \
  "$CANDIDATE_DIR/solution.mpy" \
  --definition "$WORK_DIR/concrete-kompiled" \
  --output none
run timeout 180 krun \
  "$WORK_DIR/reviewer-concrete-tests.mpy" \
  --definition "$WORK_DIR/concrete-kompiled" \
  --output none

run timeout 600 kompile \
  "$CANDIDATE_DIR/verification.k" \
  --backend haskell \
  --main-module DIGITS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK_DIR/verification-kompiled"
run timeout 600 kprove \
  "$CANDIDATE_DIR/spec.k" \
  --definition "$WORK_DIR/verification-kompiled" \
  --spec-module DIGITS-SPEC \
  --claims DIGITS-SPEC.digits-loop
run timeout 600 kprove \
  "$CANDIDATE_DIR/spec.k" \
  --definition "$WORK_DIR/verification-kompiled" \
  --spec-module DIGITS-SPEC \
  --claims DIGITS-SPEC.digits-correct
run timeout 600 kprove \
  "$CANDIDATE_DIR/spec.k" \
  --definition "$WORK_DIR/verification-kompiled" \
  --spec-module DIGITS-SPEC
