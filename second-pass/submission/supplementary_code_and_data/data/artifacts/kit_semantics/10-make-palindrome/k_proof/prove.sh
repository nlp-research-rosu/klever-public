#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled | tee smoke.out
grep -q '<k>' smoke.out
grep -q '    .K' smoke.out
grep -A2 '<exit-code>' smoke.out | grep -q '    0'

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.reverse-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.search-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY > vacuity.out 2>&1; then
  cat vacuity.out
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  status=$?
  cat vacuity.out
  test "$status" -ne 0
  echo "EXPECTED FAILURE: false-result mutation (exit $status)"
fi

kompile --backend haskell verification-mutant.k \
  --main-module VERIFICATION-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled

if kprove spec-body-mutation.k \
     --definition mutation-kompiled \
     --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1; then
  cat body-mutation.out
  echo "ERROR: mutated body unexpectedly proved" >&2
  exit 1
else
  status=$?
  cat body-mutation.out
  test "$status" -ne 0
  echo "EXPECTED FAILURE: body mutation (exit $status)"
fi

python3 test_solution.py
