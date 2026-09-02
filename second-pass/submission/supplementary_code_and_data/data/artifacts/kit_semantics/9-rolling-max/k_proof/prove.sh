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

kompile --backend haskell bind-base.k \
  --main-module BIND-BASE \
  --syntax-module BIND-BASE \
  --output-definition bind-kompiled
kprove bind-spec.k \
  --definition bind-kompiled \
  --spec-module BIND-SPEC

kompile --backend haskell loop-base.k \
  --main-module LOOP-BASE \
  --syntax-module LOOP-BASE \
  --output-definition loop-kompiled
kprove loop-spec.k \
  --definition loop-kompiled \
  --spec-module LOOP-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove loop-body-mutation.k \
     --definition loop-kompiled \
     --spec-module LOOP-BODY-MUTATION; then
  echo "ERROR: loop-body mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: loop-body mutation was rejected"
fi

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY; then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation was rejected"
fi
