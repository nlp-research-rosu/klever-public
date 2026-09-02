#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete K smoke program.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

# Required concrete execution build and smoke run.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

# Symbolic proof build and the single positive command proving every claim.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Gate A negative probes: both commands must fail.
if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY; then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION; then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: changed-body mutation"
fi

# Gate C recurrence-based differential evidence.
python3 oracle_test.py
