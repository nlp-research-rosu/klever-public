#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled

kompile verification-base.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled

kprove loop-spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove loop-witness-base.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-WITNESS-BASE

kprove loop-witness-extended.k \
  --definition verification-kompiled \
  --spec-module LOOP-WITNESS-EXTENDED

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  mutation_status=$?
  echo "EXPECTED FAILURE: false-postcondition mutation exit=${mutation_status}"
fi

if kprove loop-spec-body-mutation.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC-BODY-MUTATION
then
  echo "ERROR: body-sensitivity mutation unexpectedly proved"
  exit 1
else
  body_mutation_status=$?
  echo "EXPECTED FAILURE: body-sensitivity mutation exit=${body_mutation_status}"
fi

python3 differential_test.py
