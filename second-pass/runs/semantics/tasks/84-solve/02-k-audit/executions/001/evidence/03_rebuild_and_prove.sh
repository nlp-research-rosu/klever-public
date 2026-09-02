#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate-src
overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    overall=1
  fi
}

run kompile --version
run kprove --version
run test ! -e "$work/runtime-kompiled"
run test ! -e "$work/verification-kompiled"

run kompile "$work/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/runtime-kompiled"

run krun "$work/concrete-tests.mpy" \
  --definition "$work/runtime-kompiled" \
  --output pretty

run kompile "$work/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/verification-kompiled"

# spec.k contains the sole positive target claim (SPEC, unlabeled).
run kprove "$work/spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC \
  --output pretty

exit "$overall"
