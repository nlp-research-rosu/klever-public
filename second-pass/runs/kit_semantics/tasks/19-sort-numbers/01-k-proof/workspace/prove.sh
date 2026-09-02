#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled --output none

python3 differential_test.py
python3 py2mpy.py differential_test.py > differential_test.mpy
krun differential_test.mpy --definition runtime-kompiled --output none

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.sort-numbers

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY > vacuity.out 2>&1; then
  echo "ERROR: the deliberately false result mutation unexpectedly proved" >&2
  exit 1
else
  status=$?
  rg -q "WarnStuckClaimState" vacuity.out
  echo "expected vacuity-probe failure: exit ${status}"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1; then
  echo "ERROR: the mutated helper body unexpectedly proved" >&2
  exit 1
else
  status=$?
  rg -q "WarnStuckClaimState" body-mutation.out
  echo "expected body-mutation failure: exit ${status}"
fi
