#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 check_artifacts.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output none

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

krun concrete_tests.mpy \
  --definition verification-kompiled \
  --output none

kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-invariant

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.string-xor

python3 validation_test.py

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY; then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation rejected"
fi

if kprove spec-body-mutation.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC-BODY-MUTATION; then
  echo "ERROR: swapped-branch mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: swapped-branch mutation rejected"
fi
