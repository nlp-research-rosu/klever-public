#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd /tmp/audit-work/reconstruction || exit 125

run command -v kompile
run command -v krun
run command -v kprove
run kompile --version
run krun --version
run kprove --version
run sha256sum semantic.k verification.k spec.k solution.mpy
run test ! -e audit-concrete-llvm-kompiled
run test ! -e audit-proof-haskell-kompiled

# Concrete definition: candidate semantics only.  Although semantic.k parses
# verification.k via `requires`, this root module does not import it.
run kompile semantic.k \
  --backend llvm \
  --main-module DIGIT-SUM-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-concrete-llvm-kompiled

# Proof definition: exactly the candidate's SEMANTIC root, rebuilt from source.
run kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-proof-haskell-kompiled

# Original aggregate candidate spec. Individual targets are recorded in 03b.
run kprove spec.k \
  --definition audit-proof-haskell-kompiled \
  --spec-module SPEC
