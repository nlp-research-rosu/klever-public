#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kompile --backend haskell lemma-verification.k \
  --main-module LEMMA-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition lemma-kompiled

kprove lemma-spec.k \
  --definition lemma-kompiled \
  --spec-module LEMMA-SPEC

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-postcondition mutation was rejected"
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION; then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: body mutation was rejected"
fi

python3 differential.py

python3 py2mpy.py unicode-boundary.py > unicode-boundary.mpy
if krun unicode-boundary.mpy --definition runtime-kompiled; then
  echo "ERROR: Unicode boundary witness unexpectedly executed"
  exit 1
else
  echo "EXPECTED FAILURE: supplied chr semantics rejects code point 233"
fi
