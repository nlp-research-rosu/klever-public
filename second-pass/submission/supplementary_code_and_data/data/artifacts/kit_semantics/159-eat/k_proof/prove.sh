#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-postcondition mutation was rejected"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: changed-body mutation was rejected"
fi

python3 differential_test.py
