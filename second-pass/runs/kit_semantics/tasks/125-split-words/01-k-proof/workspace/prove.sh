#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled
python3 differential_test.py
python3 -c 'from solution import split_words; print(repr(split_words("\v")))'

kompile --backend haskell verification.k \
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

kompile --backend haskell mutation-verification.k \
  --main-module MUTATION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-verification-kompiled

if kprove spec-body-mutation.k \
     --definition mutation-verification-kompiled \
     --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: material body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: material body mutation was rejected"
fi
