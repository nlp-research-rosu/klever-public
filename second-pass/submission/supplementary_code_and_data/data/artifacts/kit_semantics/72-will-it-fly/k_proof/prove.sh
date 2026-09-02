#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 py2mpy.py model-boundary.py > model-boundary.mpy
python3 py2mpy.py model-boundary-comparison.py \
  > model-boundary-comparison.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
python3 differential_test.py
python3 model-boundary.py
python3 model-boundary-comparison.py

kompile --backend haskell verification.k \
  --main-module SUMMARY-DEFINITION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module SUM-CONNECTION
kprove connection-witness.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-WITNESS

kompile --backend haskell verification.k \
  --main-module FLOAT-REST-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition float-connection-kompiled
kprove float-connection-spec.k \
  --definition float-connection-kompiled \
  --spec-module FLOAT-SUM-CONNECTION

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kompile --backend haskell mutation-verification.k \
  --main-module SUMMARY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-postcondition mutation"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: changed-body mutation"
fi

if kprove spec-summary-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-SUMMARY-MUTATION \
  --claims SPEC-SUMMARY-MUTATION.wrong-sum
then
  echo "ERROR: wrong integer-sum interpretation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: wrong integer-sum interpretation"
fi

if kprove spec-summary-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-SUMMARY-MUTATION \
  --claims SPEC-SUMMARY-MUTATION.wrong-float-sum
then
  echo "ERROR: wrong float-sum interpretation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: wrong float-sum interpretation"
fi

if kprove spec-summary-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-SUMMARY-MUTATION \
  --claims SPEC-SUMMARY-MUTATION.wrong-reverse
then
  echo "ERROR: wrong reverse interpretation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: wrong reverse interpretation"
fi

if krun model-boundary.mpy --definition runtime-kompiled
then
  echo "ERROR: numeric-identification boundary probe unexpectedly passed"
  exit 1
else
  echo "EXPECTED FAILURE: Int/Bool equality model boundary"
fi

if krun model-boundary-comparison.mpy --definition runtime-kompiled
then
  echo "ERROR: mixed-comparison boundary probe unexpectedly passed"
  exit 1
else
  echo "EXPECTED FAILURE: mixed numeric <= model boundary"
fi
