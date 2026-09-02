#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove connection-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove context-spec.k \
  --definition verification-kompiled \
  --spec-module CONTEXT-SPEC
python3 differential_test.py

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY; then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  status=$?
  echo "EXPECTED_FAILURE spec-vacuity.k exit=$status"
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION; then
  echo "ERROR: changed-body mutation unexpectedly proved" >&2
  exit 1
else
  status=$?
  echo "EXPECTED_FAILURE spec-body-mutation.k exit=$status"
fi
