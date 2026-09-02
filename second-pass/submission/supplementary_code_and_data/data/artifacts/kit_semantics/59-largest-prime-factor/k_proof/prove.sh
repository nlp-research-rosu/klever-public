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

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

python3 differential_test.py

if kprove spec-negative.k \
  --definition verification-kompiled \
  --spec-module SPEC-NEGATIVE \
  --claims SPEC-NEGATIVE.false-post
then
  echo "ERROR: false-post mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-post"
fi

if kprove spec-negative.k \
  --definition verification-kompiled \
  --spec-module SPEC-NEGATIVE \
  --claims SPEC-NEGATIVE.body-mutation
then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: body-mutation"
fi
