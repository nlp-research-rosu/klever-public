#!/usr/bin/env bash
set -euo pipefail

python3 -m py_compile solution.py
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

rg -Fq 'Return(BinOp("%", Name("number"), Float(1.0)))' solution.mpy
rg -Fq 'Return(BinOp("%", Name("number"), Float(1.0)))' spec.k

python3 smoke.py
python3 test_solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

expect_kprove_failure() {
  local label=$1
  shift
  if "$@"; then
    echo "ERROR: ${label} unexpectedly proved"
    return 1
  else
    local status=$?
    echo "EXPECTED_FAILURE: ${label} exit=${status}"
  fi
}

expect_kprove_failure "false postcondition" \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY

expect_kprove_failure "changed function body" \
  kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION
