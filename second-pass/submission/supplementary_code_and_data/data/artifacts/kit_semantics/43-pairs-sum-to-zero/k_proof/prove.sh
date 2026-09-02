#!/usr/bin/env bash
set -euo pipefail

run_expected_failure() {
  local log_file="$1"
  shift

  set +e
  "$@" >"$log_file" 2>&1
  local command_exit=$?
  set -e

  cat "$log_file"
  if [[ $command_exit -eq 0 ]]; then
    echo "UNEXPECTED_SUCCESS: $*"
    return 1
  fi
  if rg -q 'missing hook|ErrorException' "$log_file"; then
    echo "INVALID_FAILURE_MODE: $*"
    return 1
  fi
  echo "EXPECTED_FAILURE_EXIT=$command_exit: $*"
}

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py concrete-tests.py differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled \
  | tee concrete-tests.krun.out

kompile --backend haskell connection-definition.k \
  --main-module CONNECTION-DEFINITION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled

kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

run_expected_failure spec-vacuity.out \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY

run_expected_failure spec-body-mutation.out \
  kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION

run_expected_failure connection-bad-int-equality.out \
  kprove connection-mutation-spec.k \
    --definition connection-kompiled \
    --spec-module CONNECTION-MUTATION-SPEC \
    --claims CONNECTION-MUTATION-SPEC.bad-int-equality

run_expected_failure connection-bad-int-unary-minus.out \
  kprove connection-mutation-spec.k \
    --definition connection-kompiled \
    --spec-module CONNECTION-MUTATION-SPEC \
    --claims CONNECTION-MUTATION-SPEC.bad-int-unary-minus

python3 differential_test.py | tee differential_test.out
