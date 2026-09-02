#!/usr/bin/env bash
set -euo pipefail

python3 generate_artifacts.py solution
python3 py2mpy.py solution.py > solution.mpy
python3 generate_artifacts.py k

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 generate_artifacts.py smoke
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
python3 validate.py
python3 audit_spec.py

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

python3 generate_artifacts.py mutation
kompile --backend haskell verification-mutation.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-mutation-kompiled

if kprove spec-body-mutation.k \
     --definition verification-mutation-kompiled \
     --spec-module SPEC-BODY-MUTATION
then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: body mutation was rejected"
fi
