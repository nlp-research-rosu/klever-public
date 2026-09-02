#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_test.py > concrete_test.mpy
python3 py2mpy.py body_mutation_test.py > body_mutation_test.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_test.mpy --definition runtime-kompiled > concrete.out
grep -A1 '<exit-code' concrete.out | tail -n 2

python3 differential_test.py

set +e
krun body_mutation_test.mpy \
  --definition runtime-kompiled > body_mutation.out 2>&1
body_mutation_status=$?
set -e
grep -A1 '<exit-code' body_mutation.out | tail -n 2
if [[ $body_mutation_status -eq 0 ]]; then
  echo "ERROR: body mutation unexpectedly passed"
  exit 1
fi
echo "EXPECTED BODY-MUTATION FAILURE: exit $body_mutation_status"

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant

# Run the complete spec together: the target claim consumes loop-invariant as
# its circularity. Filtering to only SPEC.sort-third would remove that proof
# dependency.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > vacuity.out 2>&1
vacuity_status=$?
set -e
sed -n '1,80p' vacuity.out
if [[ $vacuity_status -eq 0 ]]; then
  echo "ERROR: false postcondition unexpectedly proved"
  exit 1
fi
echo "EXPECTED FALSE-POSTCONDITION FAILURE: exit $vacuity_status"
