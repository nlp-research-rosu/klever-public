#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

cd /tmp/audit-work/candidate || exit 99

run kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled

run kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-haskell-kompiled

run kprove spec.k \
  --definition verification-haskell-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant \
  --output pretty

run kprove spec.k \
  --definition verification-haskell-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant,SPEC.program-correct \
  --output pretty

run kprove spec.k \
  --definition verification-haskell-kompiled \
  --spec-module SPEC \
  --output pretty
