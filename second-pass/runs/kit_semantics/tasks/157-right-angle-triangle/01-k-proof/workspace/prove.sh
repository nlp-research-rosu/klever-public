#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py solution.py | cmp - solution.mpy
python3 validation_tests.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kompile --backend llvm verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-runtime-kompiled
cmp \
  <(krun concrete-tests.mpy --definition runtime-kompiled) \
  <(krun concrete-tests.mpy --definition verification-runtime-kompiled)
echo "fixed-vs-extended LLVM outputs: identical"

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

if [ "$vacuity_status" -eq 0 ]; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
fi

echo "EXPECTED FAILURE: false-postcondition mutation exited $vacuity_status"

if [ "$body_mutation_status" -eq 0 ]; then
  echo "ERROR: mutated function body unexpectedly proved"
  exit 1
fi

echo "EXPECTED FAILURE: body mutation exited $body_mutation_status"
