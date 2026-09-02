#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled | tee krun-solution.out
krun concrete-smoke.mpy --definition runtime-kompiled | tee krun-smoke.out

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > solution-term.kore

kast \
  --expression 'Module(sumSquaresDef)' \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > verification-term.kore

cmp solution-term.kore verification-term.kore
echo "translated program and verification term are identical"

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant | tee kprove-loop.out

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --trusted SPEC.loop-invariant | tee kprove-target.out

krun concrete-smoke.mpy \
  --definition verification-kompiled | tee krun-smoke-verification.out
cmp krun-smoke.out krun-smoke-verification.out
echo "fixed and proof-extended concrete outputs are identical"

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY 2>&1 | tee vacuity.out
vacuity_status=${PIPESTATUS[0]}

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION 2>&1 | tee body-mutation.out
body_mutation_status=${PIPESTATUS[0]}

kprove spec-projection-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-PROJECTION-VACUITY 2>&1 | tee projection-mutation.out
projection_mutation_status=${PIPESTATUS[0]}
set -e

test "$vacuity_status" -ne 0
test "$body_mutation_status" -ne 0
test "$projection_mutation_status" -ne 0
rg -q 'WarnStuckClaimState' vacuity.out
rg -q 'WarnStuckClaimState' body-mutation.out
rg -q 'WarnStuckClaimState' projection-mutation.out

echo "EXPECTED FAILURE: false result (exit $vacuity_status)"
echo "EXPECTED FAILURE: mutated body (exit $body_mutation_status)"
echo "EXPECTED FAILURE: wrong projection (exit $projection_mutation_status)"
