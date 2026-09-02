#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py smoke.py differential_test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  > runtime-kompile.log 2>&1
echo "LLVM_KOMPILE_EXIT=0"

krun smoke.mpy --definition runtime-kompiled > smoke.out
rg -U -q '<k>[[:space:]]*\.K[[:space:]]*</k>' smoke.out
rg -U -q '<exit-code>[[:space:]]*0[[:space:]]*</exit-code>' smoke.out
echo "KRUN_SMOKE_EXIT=0"

kompile --backend haskell branch-connection.k \
  --main-module BRANCH-CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition branch-connection-kompiled \
  > branch-connection-kompile.log 2>&1
kprove branch-connection-spec.k \
  --definition branch-connection-kompiled \
  --spec-module BRANCH-CONNECTION-SPEC \
  2>&1 | tee branch-connection-proof.log
rg -q '^#Top$' branch-connection-proof.log

kompile --backend haskell loop-connection.k \
  --main-module LOOP-CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-connection-kompiled \
  > loop-connection-kompile.log 2>&1
kprove loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC \
  2>&1 | tee loop-connection-proof.log
rg -q '^#Top$' loop-connection-proof.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  > verification-kompile.log 2>&1
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee target-proof.log
rg -q '^#Top$' target-proof.log

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     > vacuity.log 2>&1; then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  vacuity_status=$?
fi
rg -q 'WarnStuckClaimState' vacuity.log
rg -U -q '<k>[[:space:]]*1[[:space:]]*~> \.K' vacuity.log
echo "VACUITY_EXPECTED_FAILURE_EXIT=${vacuity_status}"

kompile --backend haskell mutation.k \
  --main-module MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled \
  > mutation-kompile.log 2>&1
if kprove mutation-spec.k \
     --definition mutation-kompiled \
     --spec-module MUTATION-SPEC \
     > mutation.log 2>&1; then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
else
  mutation_status=$?
fi
rg -q 'WarnStuckClaimState' mutation.log
rg -F -q 'I +Int 2' mutation.log
echo "BODY_MUTATION_EXPECTED_FAILURE_EXIT=${mutation_status}"

python3 differential_test.py
