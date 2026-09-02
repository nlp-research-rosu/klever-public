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

run command -v kup
run kompile --version
run krun --version
run kprove --version

run kompile \
  --backend llvm \
  semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantics-kompiled \
  --warnings none || exit $?

run python3 /audit-output/evidence/03-concrete-compare.py
concrete_status=$?

run kompile \
  --backend haskell \
  verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled \
  --warnings none || exit $?

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

if [ "$proof_status" -ne 0 ]; then
  exit "$proof_status"
fi
exit "$concrete_status"
