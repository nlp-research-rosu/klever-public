#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

overall=0
run kompile /tmp/audit-work/candidate-src/semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition /tmp/audit-work/build/semantic-llvm-r2 || overall=1

run env AUDIT_K_DEFINITION=/tmp/audit-work/build/semantic-llvm-r2 \
  python3 /audit-output/evidence/k_concrete_compare.py || overall=1

run kompile /tmp/audit-work/candidate-src/verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition /tmp/audit-work/build/verification-haskell-r2 || overall=1

# Layer 1: the helper claim by itself.
run kprove /tmp/audit-work/candidate-src/spec.k \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --spec-module SPEC \
  --claims SPEC.pair-correct \
  --output pretty || overall=1

# Layer 2: helper and entry claims, excluding only the top program claim.
run kprove /tmp/audit-work/candidate-src/spec.k \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --spec-module SPEC \
  --exclude SPEC.program-correct \
  --output pretty || overall=1

# Layer 3: all three target claims, including the exact-program entry claim.
run kprove /tmp/audit-work/candidate-src/spec.k \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --spec-module SPEC \
  --output pretty || overall=1

printf '\n[script exit %d]\n' "$overall"
exit "$overall"
