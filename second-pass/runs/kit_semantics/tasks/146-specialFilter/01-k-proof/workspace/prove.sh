#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

python3 test_solution.py

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED_FAILURE: false-postcondition mutation rejected"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION; then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED_FAILURE: changed-body mutation rejected"
fi

if kprove spec-value-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-VALUE-MUTATION; then
  echo "ERROR: opposite-value mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED_FAILURE: opposite-value mutation rejected"
fi
