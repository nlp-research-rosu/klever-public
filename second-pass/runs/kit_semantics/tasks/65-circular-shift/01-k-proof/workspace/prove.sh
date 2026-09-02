#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled

python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.circular-shift-reverse

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.circular-shift-negative

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.circular-shift-rotate

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY
then
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-postcondition mutation was rejected"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: mutated program body unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: mutated program body was rejected"
fi
