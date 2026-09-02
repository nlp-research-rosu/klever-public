#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run kompile --version
run kprove --version

printf '\nFresh LLVM concrete definition from trusted supplied semantics:\n'
run timeout 600s kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/runtime-kompiled
llvm_status=$?

printf '\nFresh Haskell proof definition from trusted semantics plus candidate verification source:\n'
run timeout 600s kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled
haskell_status=$?

if (( llvm_status != 0 || haskell_status != 0 )); then
  exit 1
fi
