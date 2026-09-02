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

kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition fixed-kompiled
kprove projection-spec.k \
  --definition fixed-kompiled \
  --spec-module PROJECTION-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

if kprove connection-mutation-spec.k \
     --definition connection-kompiled \
     --spec-module CONNECTION-MUTATION-SPEC; then
  echo "ERROR: the inner-body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: the inner-body mutation was rejected"
fi

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY; then
  echo "ERROR: the false result-shape mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: the false result-shape mutation was rejected"
fi

python3 differential_test.py
