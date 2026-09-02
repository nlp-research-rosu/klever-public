#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

run kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-semantic-kompiled
semantic_status=$?

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
verification_status=$?

if (( semantic_status != 0 || verification_status != 0 )); then
  exit 1
fi
