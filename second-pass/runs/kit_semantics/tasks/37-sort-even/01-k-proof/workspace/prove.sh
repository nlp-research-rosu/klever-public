#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled
python3 test_solution.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION-NO-BRIDGE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-no-bridge-kompiled

kprove spec-connection.k \
  --definition verification-no-bridge-kompiled \
  --spec-module SPEC-CONNECTION

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
  echo "UNEXPECTED SUCCESS: false-result mutation proved"
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: false-result mutation exited ${status}"
fi

if kprove spec-body-mutation.k \
     --definition verification-no-bridge-kompiled \
     --spec-module SPEC-BODY-MUTATION; then
  echo "UNEXPECTED SUCCESS: mutated loop body proved"
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: mutated loop body exited ${status}"
fi
