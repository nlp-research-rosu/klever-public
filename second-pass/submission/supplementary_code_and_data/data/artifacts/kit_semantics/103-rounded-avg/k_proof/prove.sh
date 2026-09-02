#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 test_solution.py
python3 py2mpy.py smoke.py > smoke.mpy
proof_tmp=$(mktemp -d)
trap 'rm -r -- "$proof_tmp"' EXIT

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled > "$proof_tmp/fixed-smoke.out"
cat "$proof_tmp/fixed-smoke.out"

kompile --backend haskell arithmetic-verification.k \
  --main-module ARITHMETIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition arithmetic-kompiled
kprove arithmetic-spec.k \
  --definition arithmetic-kompiled \
  --spec-module ARITHMETIC-SPEC

kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module LOOP-CONNECTION
kprove rounding-spec.k \
  --definition connection-kompiled \
  --spec-module ROUNDING-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
krun smoke.mpy --definition verification-kompiled > "$proof_tmp/bridged-smoke.out"
cmp "$proof_tmp/fixed-smoke.out" "$proof_tmp/bridged-smoke.out"
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.rounded-avg-invalid
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.rounded-avg-valid

expect_failure() {
  local label=$1
  shift
  set +e
  "$@"
  local status=$?
  set -e
  echo "${label}_EXIT:${status}"
  if [[ ${status} -eq 0 ]]; then
    echo "${label}: unexpected success" >&2
    exit 1
  fi
}

expect_failure VACUITY \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY
expect_failure BODY_MUTATION \
  kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION
expect_failure CONNECTION_MUTATION \
  kprove connection-body-mutation.k \
    --definition connection-kompiled \
    --spec-module LOOP-CONNECTION-MUTATION
