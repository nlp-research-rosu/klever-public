#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 test_solution.py | tee python-differential.out

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled > krun-smoke.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee target-proof.out

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     > vacuity-proof.out 2>&1; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: false-postcondition mutation exited ${status}"
fi

if kprove spec-body-mutant.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTANT \
     > body-mutant-proof.out 2>&1; then
  echo "ERROR: mutated body unexpectedly proved"
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: mutated body exited ${status}"
fi
