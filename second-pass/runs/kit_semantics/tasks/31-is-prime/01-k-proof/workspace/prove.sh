#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  | tee concrete-tests.krun.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  | tee all-claims.kprove.out

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation.kprove.out 2>&1
body_mutation_status=$?

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.kprove.out 2>&1
vacuity_status=$?
set -e

if [[ $body_mutation_status -eq 0 ]]; then
  echo "Body mutation unexpectedly proved." >&2
  exit 1
fi
echo "Body mutation: EXPECTED FAILURE (exit $body_mutation_status)"

if [[ $vacuity_status -eq 0 ]]; then
  echo "False postcondition unexpectedly proved." >&2
  exit 1
fi
echo "False postcondition: EXPECTED FAILURE (exit $vacuity_status)"

python3 differential_test.py | tee differential-test.out
