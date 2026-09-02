#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

run kompile semantic-driver.k \
  --main-module AUDIT-DRIVER \
  --syntax-module AUDIT-DRIVER \
  --backend haskell \
  --output-definition audit-driver-haskell-kompiled
run krun audit-normal.mpy \
  --definition audit-driver-haskell-kompiled \
  --output pretty
run krun audit-zero.mpy \
  --definition audit-driver-haskell-kompiled \
  --output pretty
run krun audit-all-fruit.mpy \
  --definition audit-driver-haskell-kompiled \
  --output pretty

run krun audit-verification-normal.mpy \
  --definition audit-verification-kompiled \
  --output pretty
run krun audit-verification-zero.mpy \
  --definition audit-verification-kompiled \
  --output pretty
run krun audit-verification-all-fruit.mpy \
  --definition audit-verification-kompiled \
  --output pretty
