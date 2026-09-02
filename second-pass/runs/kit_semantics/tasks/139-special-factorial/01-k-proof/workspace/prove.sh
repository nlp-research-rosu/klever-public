#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py body-mutation.py > body-mutation.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled | tee krun-smoke.out
python3 test_solution.py | tee differential.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC 2>&1 | tee proof.out

kprove summary-test.k \
  --definition verification-kompiled \
  --spec-module SUMMARY-TEST 2>&1 | tee summary-test.out

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY > vacuity.out 2>&1; then
  cat vacuity.out
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
fi
grep -q "WarnStuckClaimState" vacuity.out
grep -Fq "productAfter ( 2 , N , 1 , 1 ) +Int 1" vacuity.out
echo "false-postcondition mutation: expected failure"

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1; then
  cat body-mutation.out
  echo "ERROR: changed-body mutation unexpectedly proved" >&2
  exit 1
fi
grep -q "WarnStuckClaimState" body-mutation.out
grep -Fq "R *Int ( F *Int I ) +Int 1" body-mutation.out
echo "changed-body mutation: expected failure"
