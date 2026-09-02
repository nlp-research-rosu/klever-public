#!/usr/bin/env bash
set -euo pipefail

expect_failure() {
  local label="$1"
  shift

  set +e
  "$@"
  local status=$?
  set -e

  if [[ $status -eq 0 ]]; then
    echo "UNEXPECTED SUCCESS: $label"
    exit 1
  fi
  echo "EXPECTED FAILURE: $label (exit $status)"
}

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py smoke.py differential_test.py
python3 smoke.py
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled > krun-smoke.out
rg -q '^    \.K$' krun-smoke.out

kompile --backend haskell shape-connection.k \
  --main-module SHAPE-CONNECTION \
  --syntax-module ROW-MODEL-SYNTAX \
  --output-definition shape-connection-kompiled
kprove shape-connection-spec.k \
  --definition shape-connection-kompiled \
  --spec-module SHAPE-CONNECTION-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kompile --backend haskell mutation.k \
  --main-module MUTATION \
  --syntax-module MUTATION-SYNTAX \
  --output-definition mutation-kompiled

expect_failure "wrong returned reference" \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY
expect_failure "coordinate-append body mutation" \
  kprove spec-body-mutation.k \
    --definition mutation-kompiled \
    --spec-module SPEC-BODY-MUTATION
expect_failure "incorrect For bridge result" \
  kprove shape-connection-bad-spec.k \
    --definition shape-connection-kompiled \
    --spec-module SHAPE-CONNECTION-BAD-SPEC

echo "All positive proofs passed and all negative probes failed as expected."
