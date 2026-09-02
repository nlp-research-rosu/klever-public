#!/usr/bin/env bash
set -eu

expect_failure() {
  probe_name=$1
  shift
  if "$@"; then
    echo "UNEXPECTED SUCCESS: ${probe_name}" >&2
    exit 1
  else
    probe_status=$?
    echo "EXPECTED FAILURE: ${probe_name} (exit ${probe_status})"
  fi
}

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Bridge-free projection, yield, and inner-loop connection proofs.
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

# Outer-loop connection proof, using only the already-connected inner bridge.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition outer-connection-kompiled
kprove outer-connection-spec.k \
  --definition outer-connection-kompiled \
  --spec-module OUTER-CONNECTION-SPEC

# Full target proof: both unbounded loop claims and both whole-program entries.
kompile --backend haskell verification.k \
  --main-module TARGET-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Gate A negative probes.
expect_failure false-result \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY

expect_failure inner-wrong-value \
  kprove bridge-mutation-spec.k \
    --definition connection-kompiled \
    --spec-module BRIDGE-MUTATION-SPEC \
    --claims BRIDGE-MUTATION-SPEC.inner-wrong-value

expect_failure yield-wrong-value \
  kprove bridge-mutation-spec.k \
    --definition connection-kompiled \
    --spec-module BRIDGE-MUTATION-SPEC \
    --claims BRIDGE-MUTATION-SPEC.yield-wrong-value

kompile --backend haskell mutation-verification.k \
  --main-module MUTATION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled
expect_failure changed-body \
  kprove mutation-spec.k \
    --definition mutation-kompiled \
    --spec-module MUTATION-SPEC
