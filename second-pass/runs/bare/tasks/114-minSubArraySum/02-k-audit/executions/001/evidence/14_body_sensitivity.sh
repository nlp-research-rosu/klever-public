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

run kompile \
  --backend haskell \
  verification-body-mutated.k \
  --main-module VERIFICATION-BODY-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutated-kompiled

run krun solution-body-mutated.mpy \
  --definition semantic-audit-kompiled \
  '-cENTRY="minSubArraySum"' \
  '-cARGS=pyList(cons(7, nil))'

run kprove spec-body-mutated.k \
  --definition verification-body-mutated-kompiled \
  --spec-module SPEC-BODY-MUTATED \
  --dry-run

run kprove spec-body-mutated.k \
  --definition verification-body-mutated-kompiled \
  --spec-module SPEC-BODY-MUTATED
