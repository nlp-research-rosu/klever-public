#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

SOURCE=/tmp/audit-work/114-minSubArraySum-audit
DEST=/audit-output/evidence

run cp "$SOURCE/spec-labeled.k" "$DEST/spec-labeled.k"
run cp "$SOURCE/spec-prefix-only.k" "$DEST/spec-prefix-only.k"
run cp "$SOURCE/spec-target-suite.k" "$DEST/spec-target-suite.k"
run cp "$SOURCE/spec-direct-program.k" "$DEST/spec-direct-program.k"
run cp "$SOURCE/spec-vacuity-audit.k" "$DEST/spec-vacuity-audit.k"
run cp "$SOURCE/semantic-no-fused.k" "$DEST/semantic-no-fused.k"
run cp "$SOURCE/verification-body-mutated.k" "$DEST/verification-body-mutated.k"
run cp "$SOURCE/spec-body-mutated.k" "$DEST/spec-body-mutated.k"
run cp "$SOURCE/solution-body-mutated.mpy" "$DEST/solution-body-mutated.mpy"
run diff -u "$SOURCE/semantic.k" "$SOURCE/semantic-no-fused.k"
run diff -u "$SOURCE/verification.k" "$SOURCE/verification-body-mutated.k"
run diff -u "$SOURCE/solution.mpy" "$SOURCE/solution-body-mutated.mpy"
run sha256sum \
  "$DEST/spec-labeled.k" \
  "$DEST/spec-prefix-only.k" \
  "$DEST/spec-target-suite.k" \
  "$DEST/spec-direct-program.k" \
  "$DEST/spec-vacuity-audit.k" \
  "$DEST/semantic-no-fused.k" \
  "$DEST/verification-body-mutated.k" \
  "$DEST/spec-body-mutated.k" \
  "$DEST/solution-body-mutated.mpy"
