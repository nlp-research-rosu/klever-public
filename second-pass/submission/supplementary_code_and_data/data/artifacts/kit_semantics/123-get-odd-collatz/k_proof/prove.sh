#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.nix-profile/bin:$PATH"

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-smoke.mpy --definition runtime-kompiled
python3 test_differential.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.collatz-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_status=$?

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_mutation_status=$?
set -e

if [[ "$vacuity_status" -eq 0 ]]; then
  echo "UNEXPECTED SUCCESS: false-result mutation"
  exit 1
fi
echo "EXPECTED FAILURE: false-result mutation exited $vacuity_status"

if [[ "$body_mutation_status" -eq 0 ]]; then
  echo "UNEXPECTED SUCCESS: mutated-body probe"
  exit 1
fi
echo "EXPECTED FAILURE: mutated-body probe exited $body_mutation_status"
