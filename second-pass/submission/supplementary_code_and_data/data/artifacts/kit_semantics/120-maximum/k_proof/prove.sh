#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 identity_check.py
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 py2mpy.py boundary-test.py > boundary-test.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none

krun boundary-test.mpy \
  --definition runtime-kompiled \
  --output none

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
  printf '%s\n' 'ERROR: false-result mutation unexpectedly proved'
  exit 1
else
  printf '%s\n' 'EXPECTED_FAILURE: false-result mutation was rejected'
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION; then
  printf '%s\n' 'ERROR: mutated body unexpectedly proved the original result'
  exit 1
else
  printf '%s\n' 'EXPECTED_FAILURE: body mutation was rejected'
fi

python3 differential_test.py
