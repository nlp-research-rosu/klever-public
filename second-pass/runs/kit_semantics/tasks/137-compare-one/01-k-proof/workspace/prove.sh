#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py model_boundary_probe.py > model_boundary_probe.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled | tee krun-smoke.out
python3 differential_test.py | tee differential.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

krun solution.mpy \
  --definition verification-kompiled \
  --output kore > solution-direct.kore
krun solution-module.term \
  --definition verification-kompiled \
  --parser ./parse-verification-module.sh \
  --output kore > solution-named.kore
cmp solution-direct.kore solution-named.kore
echo "AST IDENTITY: solutionModule() matches solution.mpy"

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee kprove.out

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY > vacuity.out 2>&1; then
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-postcondition mutation"
fi

if kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1; then
  echo "ERROR: changed-body mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: changed-body mutation"
fi

python3 model_boundary_probe.py
if krun model_boundary_probe.mpy \
    --definition runtime-kompiled > model-boundary.out 2>&1; then
  echo "ERROR: model-boundary probe unexpectedly agreed" >&2
  exit 1
else
  echo "EXPECTED FAILURE: supplied decimal parser differs on exponent notation"
fi
