#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py krun_tests.py > krun_tests.mpy
python3 test_solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled > krun-solution.out
krun krun_tests.mpy --definition runtime-kompiled > krun-tests.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.is-multiply-prime \
  2>&1 | tee positive-proof.out

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-postcondition \
  > vacuity.out 2>&1
vacuity_status=$?

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.changed-body \
  > body-mutation.out 2>&1
body_mutation_status=$?
set -e

if [ "$vacuity_status" -eq 0 ]; then
  echo "false-postcondition mutation unexpectedly proved" >&2
  exit 1
fi

if [ "$body_mutation_status" -eq 0 ]; then
  echo "changed-body mutation unexpectedly proved" >&2
  exit 1
fi

printf 'vacuity mutation: EXPECTED FAILURE (exit %s)\n' "$vacuity_status"
printf 'body mutation: EXPECTED FAILURE (exit %s)\n' "$body_mutation_status"
