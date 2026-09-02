#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 test_solution.py

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

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY; then
  echo "ERROR: false-postcondition probe unexpectedly passed"
  exit 1
else
  echo "EXPECTED FAILURE: false-postcondition probe was rejected"
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION; then
  echo "ERROR: body-mutation probe unexpectedly passed"
  exit 1
else
  echo "EXPECTED FAILURE: body-mutation probe was rejected"
fi
