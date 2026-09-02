#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 audit_identity.py
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

expect_failure() {
  local label=$1
  shift
  local probe_status

  set +e
  "$@"
  probe_status=$?
  set -e

  if [[ $probe_status -eq 0 ]]; then
    echo "UNEXPECTED SUCCESS: $label"
    return 1
  fi
  echo "EXPECTED FAILURE: $label (exit $probe_status)"
}

expect_failure "false result / non-vacuity probe" \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY

expect_failure "ROT5 body-sensitivity probe" \
  kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION
