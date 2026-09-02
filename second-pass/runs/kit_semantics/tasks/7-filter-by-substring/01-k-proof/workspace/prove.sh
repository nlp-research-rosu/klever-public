#!/usr/bin/env bash
set -eu

expect_failure() {
  description=$1
  shift
  if "$@"; then
    echo "UNEXPECTED SUCCESS: ${description}" >&2
    exit 1
  else
    status=$?
    echo "EXPECTED FAILURE: ${description} (exit ${status})"
  fi
}

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove spec-value-check.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-CHECK

expect_failure "false result postcondition" \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY

expect_failure "material body mutation" \
  kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION

expect_failure "opposite strCodes interpretation" \
  kprove spec-value-opposite.k \
    --definition verification-kompiled \
    --spec-module SPEC-VALUE-OPPOSITE

python3 differential_test.py
