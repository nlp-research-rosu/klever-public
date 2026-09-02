#!/bin/sh
set -eu

expect_failure() {
  label=$1
  shift
  if "$@"; then
    echo "UNEXPECTED SUCCESS: $label" >&2
    exit 1
  else
    status=$?
    echo "EXPECTED FAILURE: $label (exit $status)"
  fi
}

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module MAX-FILL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC
krun smoke.mpy --definition verification-kompiled

kompile --backend haskell verification.k \
  --main-module MAX-FILL-SUMMARY \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module MAX-FILL-CONNECTION-SPEC

expect_failure false-result \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module MAX-FILL-VACUITY-SPEC
expect_failure mutated-body \
  kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module MAX-FILL-BODY-MUTATION-SPEC
expect_failure wrong-int-projection \
  kprove projection-mutation-spec.k \
    --definition connection-kompiled \
    --spec-module MAX-FILL-PROJECTION-MUTATION-SPEC \
    --claims MAX-FILL-PROJECTION-MUTATION-SPEC.wrong-int
expect_failure wrong-row-projection \
  kprove projection-mutation-spec.k \
    --definition connection-kompiled \
    --spec-module MAX-FILL-PROJECTION-MUTATION-SPEC \
    --claims MAX-FILL-PROJECTION-MUTATION-SPEC.wrong-row
