#!/usr/bin/env bash
set -u -o pipefail

SCRATCH=/tmp/audit-work/141-file-name-check
cd "$SCRATCH" || exit 1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run kompile \
  --backend haskell \
  verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled \
  --warnings none || exit $?

# Cross-check the boundary witness under the proof backend too.
run krun \
  solution.mpy \
  --definition audit-verification-kompiled \
  '-cINPUT=""'
haskell_empty_status=$?

run kprove \
  spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --warnings all
proof_status=$?

printf '\n$ %s\n' "rg -n '^[[:space:]]*claim\\b' spec.k verification.k semantic.k"
rg -n '^[[:space:]]*claim\b' spec.k verification.k semantic.k
inventory_status=$?
printf '[exit %d]\n' "$inventory_status"

exit "$proof_status"
