#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
python3 concrete-smoke.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-smoke.mpy \
  --definition runtime-kompiled \
  | tee concrete-smoke.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee proof-main.out

kprove spec-summary.k \
  --definition verification-kompiled \
  --spec-module SPEC-SUMMARY \
  2>&1 | tee proof-summary.out

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     > proof-vacuity.out 2>&1; then
  echo "UNEXPECTED SUCCESS: false-postcondition probe"
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: false-postcondition probe (exit $status)"
fi

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION \
     > proof-body-mutation.out 2>&1; then
  echo "UNEXPECTED SUCCESS: body-mutation probe"
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: body-mutation probe (exit $status)"
fi

python3 differential_test.py | tee differential-test.out
