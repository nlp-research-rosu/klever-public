#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.empty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.nonempty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY \
    > vacuity.out 2>&1
then
  cat vacuity.out
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
else
  mutation_status=$?
  cat vacuity.out
  if [ "$mutation_status" -ne 1 ] ||
     ! rg -q "WarnStuckClaimState" vacuity.out
  then
    echo "ERROR: false-result mutation failed for an unexpected reason"
    exit 1
  fi
  echo "EXPECTED FAILURE: false-result mutation (exit 1)"
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION \
    > body-mutation.out 2>&1
then
  cat body-mutation.out
  echo "ERROR: mutated body unexpectedly proved"
  exit 1
else
  mutation_status=$?
  cat body-mutation.out
  if [ "$mutation_status" -ne 1 ] ||
     ! rg -q "WarnStuckClaimState" body-mutation.out
  then
    echo "ERROR: body mutation failed for an unexpected reason"
    exit 1
  fi
  echo "EXPECTED FAILURE: body mutation (exit 1)"
fi
