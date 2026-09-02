#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py smoke.py test_solution.py
python3 test_solution.py | tee differential.out

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled | tee krun-smoke.out
rg -U '<k>[[:space:]]+\.K[[:space:]]+</k>' krun-smoke.out > /dev/null

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee proof-positive.out
rg '^#Top$' proof-positive.out > /dev/null

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY 2>&1 | tee vacuity.out
vacuity_status=${PIPESTATUS[0]}
set -e
printf '%s\n' "$vacuity_status" > vacuity.exit
test "$vacuity_status" -eq 1
rg 'WarnStuckClaimState' vacuity.out > /dev/null

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION 2>&1 | tee body-mutation.out
body_status=${PIPESTATUS[0]}
set -e
printf '%s\n' "$body_status" > body-mutation.exit
test "$body_status" -eq 1
rg 'WarnStuckClaimState' body-mutation.out > /dev/null

printf 'all positive checks passed; both negative probes failed as expected\n'
