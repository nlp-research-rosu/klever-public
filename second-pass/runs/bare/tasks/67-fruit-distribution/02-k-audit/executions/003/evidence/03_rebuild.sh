#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/fruit67/candidate
cd "$work" || exit 99

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

run kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition audit-semantic-llvm-kompiled || exit $?

run krun solution.mpy \
  --definition audit-semantic-llvm-kompiled \
  --output pretty || exit $?

run kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend llvm \
  --output-definition audit-verification-llvm-kompiled || exit $?

run kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition audit-verification-haskell-kompiled || exit $?

run kprove spec.k \
  --definition audit-verification-haskell-kompiled \
  --spec-module SPEC
