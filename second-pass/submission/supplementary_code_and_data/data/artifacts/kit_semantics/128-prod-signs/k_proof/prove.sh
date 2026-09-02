#!/usr/bin/env bash
set -eu

run_expected_failure() {
  check_name=$1
  shift

  set +e
  "$@"
  check_status=$?
  set -e

  if [ "$check_status" -eq 0 ]; then
    echo "$check_name UNEXPECTED_SUCCESS"
    exit 1
  fi

  echo "$check_name EXPECTED_NONZERO_EXIT=$check_status"
}

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell connection.k \
  --main-module CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

kompile --backend haskell loop-connection.k \
  --main-module LOOP-CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-connection-kompiled
kprove loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC
kprove iterator-witness-spec.k \
  --definition loop-connection-kompiled \
  --spec-module ITERATOR-WITNESS-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

run_expected_failure \
  CONNECTION_VALUE_MUTATION \
  kprove connection-mutation-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-MUTATION-SPEC

run_expected_failure \
  LOOP_BODY_MUTATION \
  kprove loop-body-mutation-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-BODY-MUTATION-SPEC

run_expected_failure \
  FALSE_POSTCONDITION \
  kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

python3 differential_test.py
