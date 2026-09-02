#!/usr/bin/env bash
set -u
cd /tmp/audit-work/candidate

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run kompile --version || exit $?
run kprove --version || exit $?
run krun --version || exit $?

run kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/candidate/semantic-kompiled || exit $?

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/candidate/verification-kompiled || exit $?

run kprove spec.k \
  --definition /tmp/audit-work/candidate/verification-kompiled \
  --spec-module SPEC
