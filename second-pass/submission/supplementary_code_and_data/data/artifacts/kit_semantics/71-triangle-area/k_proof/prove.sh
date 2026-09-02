#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 test_solution.py
python3 check_artifacts.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled | tee krun-smoke.log

python3 model-boundary.py | tee model-boundary-python.log
krun model-boundary.mpy --definition runtime-kompiled \
  | tee model-boundary-krun.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee kprove-all.log
grep -q '^#Top$' kprove-all.log

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     > kprove-vacuity.log 2>&1; then
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
fi
grep -q 'WarnStuckClaimState' kprove-vacuity.log
! grep -q 'missing hook' kprove-vacuity.log
echo "EXPECTED FAILURE: false-postcondition mutation"

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION \
     > kprove-body-mutation.log 2>&1; then
  echo "ERROR: mutated body unexpectedly proved" >&2
  exit 1
fi
grep -q 'WarnStuckClaimState' kprove-body-mutation.log
! grep -q 'missing hook' kprove-body-mutation.log
echo "EXPECTED FAILURE: body mutation"
