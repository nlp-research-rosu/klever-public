#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 check_artifacts.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled | tee krun-smoke.out
grep -Fq '"result_1" |-> 0' krun-smoke.out
grep -Fq '"result_5" |-> 1' krun-smoke.out
grep -Fq '"result_10" |-> 36' krun-smoke.out
grep -Fq '<exit-code>' krun-smoke.out

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee kprove-positive.out
grep -qx '#Top' kprove-positive.out

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > kprove-vacuity.out 2>&1
then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  vacuity_status=$?
fi
cat kprove-vacuity.out
grep -q 'WarnStuckClaimState' kprove-vacuity.out
echo "EXPECTED FAILURE: false-postcondition mutation exit=${vacuity_status}"

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > kprove-body-mutation.out 2>&1
then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
else
  body_status=$?
fi
cat kprove-body-mutation.out
grep -q 'WarnStuckClaimState' kprove-body-mutation.out
echo "EXPECTED FAILURE: changed-body mutation exit=${body_status}"

python3 validate.py
