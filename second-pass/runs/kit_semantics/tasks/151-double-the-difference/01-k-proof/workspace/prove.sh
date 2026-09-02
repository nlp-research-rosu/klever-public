#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 py2mpy.py model-boundary-bool.py > model-boundary-bool.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled
krun model-boundary-bool.mpy --definition runtime-kompiled
python3 -c 'from solution import double_the_difference; print(double_the_difference([True]))'
python3 test_solution.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY 2>&1 | tee vacuity.log; then
  echo "ERROR: false postcondition unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false postcondition was rejected"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION 2>&1 | tee body-mutation.log; then
  echo "ERROR: changed body unexpectedly proved the original result"
  exit 1
else
  echo "EXPECTED FAILURE: changed body was rejected"
fi
