#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive
failed=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    failed=1
  fi
}

run kompile "$work/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition "$work/verification-kompiled"

run kprove "$work/spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC \
  --claims SPEC.filter-loop \
  --smt-timeout 10000

run kprove "$work/spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC \
  --claims SPEC.get-positive-correct \
  --smt-timeout 10000

run kprove "$work/spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC \
  --smt-timeout 10000

exit "$failed"
