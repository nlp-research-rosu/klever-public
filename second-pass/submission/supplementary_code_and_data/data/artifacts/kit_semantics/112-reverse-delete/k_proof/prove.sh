#!/usr/bin/env bash
set -euo pipefail

# Translation freshness and ordinary Python syntax.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py differential.py check_identity.py
python3 check_identity.py | tee identity.out

# Concrete execution under the supplied LLVM semantics.
python3 py2mpy.py smoke.py > smoke.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled | tee smoke.out
python3 differential.py --definition runtime-kompiled \
  | tee differential.out

# Symbolic proof under MPY (without the concrete-only MPY-CONCRETE module).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  | tee proof-positive.out
grep -qx '#Top' proof-positive.out

# Gate A5: the deliberately false result must not prove.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > proof-vacuity.out 2>&1
vacuity_status=$?
set -e
if [[ $vacuity_status -eq 0 ]]; then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
fi
grep -q 'WarnStuckClaimState' proof-vacuity.out
echo "EXPECTED FAILURE: false-result mutation (exit $vacuity_status)"

# Gate A1: a material body mutation must invalidate the original result.
set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > proof-body-mutation.out 2>&1
body_status=$?
set -e
if [[ $body_status -eq 0 ]]; then
  echo "ERROR: changed-body mutation unexpectedly proved"
  exit 1
fi
grep -q 'WarnStuckClaimState' proof-body-mutation.out
echo "EXPECTED FAILURE: changed-body mutation (exit $body_status)"
