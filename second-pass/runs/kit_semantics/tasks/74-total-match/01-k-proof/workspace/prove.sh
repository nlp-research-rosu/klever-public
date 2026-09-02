#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

python3 differential_test.py

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_status=$?

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_mutation_status=$?
set -e

if [ "$vacuity_status" -eq 0 ]; then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
fi
echo "EXPECTED FAILURE: false-result mutation exited $vacuity_status"

if [ "$body_mutation_status" -eq 0 ]; then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
fi
echo "EXPECTED FAILURE: body mutation exited $body_mutation_status"
