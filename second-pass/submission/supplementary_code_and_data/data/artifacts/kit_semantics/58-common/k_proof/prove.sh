#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
krun concrete-smoke.mpy --definition runtime-kompiled
python3 validate.py

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
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation"
fi

if kprove spec-value-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION
then
  echo "ERROR: false-summary-value mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-summary-value mutation"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: duplicate-body mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: duplicate-body mutation"
fi
