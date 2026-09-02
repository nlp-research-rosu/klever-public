#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 check_body_identity.py
python3 differential_test.py
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove loop-spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC

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
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation was rejected"
fi

if kprove body-mutation-spec.k \
  --definition verification-base-kompiled \
  --spec-module BODY-MUTATION-SPEC
then
  echo "ERROR: empty-loop-body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: empty-loop-body mutation was rejected"
fi
