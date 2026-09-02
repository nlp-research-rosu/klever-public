#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 check_program_identity.py
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py smoke.py differential_test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled | tee krun-solution.out
krun smoke.mpy --definition runtime-kompiled | tee krun-smoke.out
python3 differential_test.py | tee differential-test.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-inv | tee kprove-loop.out

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee kprove.out

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY 2>&1 | tee vacuity.out
vacuity_status=${PIPESTATUS[0]}
set -e
if [[ ${vacuity_status} -eq 0 ]]; then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
fi
echo "EXPECTED FAILURE: false-result mutation exited ${vacuity_status}"

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION 2>&1 | tee body-mutation.out
body_mutation_status=${PIPESTATUS[0]}
set -e
if [[ ${body_mutation_status} -eq 0 ]]; then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
fi
echo "EXPECTED FAILURE: changed-body mutation exited ${body_mutation_status}"
