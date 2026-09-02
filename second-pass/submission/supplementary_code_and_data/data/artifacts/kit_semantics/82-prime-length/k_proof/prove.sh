#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
python3 evidence.py

kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-smoke.mpy --definition runtime-kompiled \
  | tee concrete-smoke.out
rg -U '<exc>\s+NoExc\s+</exc>' concrete-smoke.out
rg -U '<exit-code>\s+0\s+</exit-code>' concrete-smoke.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled --spec-module SPEC \
  | tee positive-proof.out
rg -x '#Top' positive-proof.out

expect_stuck() {
  local log=$1
  shift
  if "$@" > "$log" 2>&1; then
    echo "UNEXPECTED SUCCESS: $*"
    return 1
  fi
  rg 'WarnStuckClaimState' "$log"
  echo "EXPECTED FAILURE: $*"
}

expect_stuck vacuity-two.log \
  kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.length-two-not-prime

expect_stuck vacuity-four.log \
  kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.length-four-prime

expect_stuck body-mutation.log \
  kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.mutated-length-two
