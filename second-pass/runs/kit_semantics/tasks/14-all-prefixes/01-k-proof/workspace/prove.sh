#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy
python3 test_solution.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee kompile-llvm.out

python3 py2mpy.py concrete-validation.py > concrete-validation.mpy
krun concrete-validation.mpy \
  --definition runtime-kompiled \
  2>&1 | tee krun.out

rg -Uq '<k>[[:space:]]+\.K[[:space:]]+</k>' krun.out
rg -Uq '<exc>[[:space:]]+NoExc[[:space:]]+</exc>' krun.out
rg -Uq '<exit-code>[[:space:]]+0[[:space:]]+</exit-code>' krun.out

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee kompile-haskell.out

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant \
  2>&1 | tee kprove-loop.out
rg -q '^#Top$' kprove-loop.out

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee kprove.out
rg -q '^#Top$' kprove.out

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.out 2>&1
vacuity_status=$?
set -e
if [[ "$vacuity_status" -ne 1 ]]; then
  sed -n '1,240p' vacuity.out
  echo "Expected spec-vacuity.k to exit 1, got $vacuity_status" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' vacuity.out
rg -q 'AssertionError' vacuity.out
echo "spec-vacuity.k: expected rejection (exit 1, AssertionError)"

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation.out 2>&1
body_status=$?
set -e
if [[ "$body_status" -ne 1 ]]; then
  sed -n '1,240p' body-mutation.out
  echo "Expected spec-body-mutation.k to exit 1, got $body_status" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' body-mutation.out
rg -q 'AssertionError' body-mutation.out
echo "spec-body-mutation.k: expected rejection (exit 1, AssertionError)"
