#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work/46-fib4-review || exit 99

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run test ! -e reviewer-runtime-kompiled
run test ! -e reviewer-verification-kompiled
run kompile --version
run kprove --version

run timeout 900 kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled

run timeout 300 krun concrete-tests.mpy \
  --definition reviewer-runtime-kompiled

run timeout 900 kompile verification.k \
  --backend haskell \
  --main-module FIB4-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled

run timeout 900 kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC \
  --claims FIB4-SPEC.loop-step \
  --output pretty

run timeout 900 kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC \
  --claims FIB4-SPEC.operational-cases \
  --output pretty
