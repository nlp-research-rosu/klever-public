#!/usr/bin/env bash
set -u

work=/tmp/audit-work/46-fib4-audit/candidate-src
evidence=/audit-output/evidence

run_logged() {
  local tag=$1
  shift
  local log="$evidence/$tag.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "$log"
  local rc=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$rc" | tee -a "$log"
  return 0
}

cd "$work" || exit 99

run_logged stage3_prebuild_inventory \
  find . -maxdepth 2 -printf '%y %p -> %l\n'

run_logged stage3_llvm_build timeout 300s \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

run_logged stage3_haskell_build timeout 300s \
  kompile verification.k \
  --backend haskell \
  --main-module FIB4-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

run_logged stage3_prove_loop_step timeout 300s \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module FIB4-SPEC \
  --claims FIB4-SPEC.loop-step \
  --output pretty

run_logged stage3_prove_operational_cases timeout 300s \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module FIB4-SPEC \
  --claims FIB4-SPEC.operational-cases \
  --output pretty
