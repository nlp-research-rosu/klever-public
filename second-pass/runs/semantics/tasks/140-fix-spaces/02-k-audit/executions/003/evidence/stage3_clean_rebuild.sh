#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/140-fix-spaces/source
cd "$scratch" || exit 90

failures=0

run_command() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'exit=%s\n' "$status"
  if [ "$status" -ne 0 ]; then
    failures=$((failures + 1))
  fi
}

run_command kompile --version
run_command kprove --version
run_command krun --version

run_command kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled

run_command krun concrete-tests.mpy \
  --definition fresh-runtime-kompiled

run_command kompile verification.k \
  --backend haskell \
  --main-module FIX-SPACES-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-proof-base-kompiled

run_command kprove spec.k \
  --definition fresh-proof-base-kompiled \
  --spec-module FIX-SPACES-FLUSH-SPEC

run_command kompile verification.k \
  --backend haskell \
  --main-module FIX-SPACES-FLUSH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-proof-step-kompiled

run_command kprove spec.k \
  --definition fresh-proof-step-kompiled \
  --spec-module FIX-SPACES-STEP-SPEC

run_command kompile verification.k \
  --backend haskell \
  --main-module FIX-SPACES-STEP-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-proof-loop-kompiled

run_command kprove spec.k \
  --definition fresh-proof-loop-kompiled \
  --spec-module FIX-SPACES-LOOP-SPEC

run_command kompile verification.k \
  --backend haskell \
  --main-module FIX-SPACES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-proof-main-kompiled

run_command kprove spec.k \
  --definition fresh-proof-main-kompiled \
  --spec-module FIX-SPACES-MAIN-SPEC

printf 'command_failures=%s\n' "$failures"
exit "$failures"
