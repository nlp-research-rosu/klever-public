#!/usr/bin/env bash
set -u

SOURCE=/tmp/audit-work/99-closest-integer/source
BUILD=/tmp/audit-work/99-closest-integer/build
SEMANTIC_DEFINITION="$BUILD/semantic-fresh-kompiled"
VERIFICATION_DEFINITION="$BUILD/verification-fresh-kompiled"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return 0
}

run find "$SOURCE" -maxdepth 1 -type d -name '*-kompiled' -print

run kompile "$SOURCE/semantic.k" \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$SEMANTIC_DEFINITION"

run python3 /audit-output/evidence/concrete_compare.py

run kompile "$SOURCE/verification.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$VERIFICATION_DEFINITION"

run kprove "$SOURCE/spec.k" \
  --definition "$VERIFICATION_DEFINITION" \
  --spec-module SPEC

run cp /audit-output/evidence/spec-audit.k "$SOURCE/spec-audit.k"

for number in 01 02 03 04 05 06 07 08 09 10 11; do
  run kprove "$SOURCE/spec-audit.k" \
    --definition "$VERIFICATION_DEFINITION" \
    --spec-module SPEC-AUDIT \
    --claims "SPEC-AUDIT.audit-$number"
done
