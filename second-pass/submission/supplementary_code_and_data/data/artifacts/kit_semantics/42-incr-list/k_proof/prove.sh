#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py differential.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled > concrete.out
awk '
  /<exit-code>/ {
    getline
    if ($1 == "0") {
      found_zero = 1
    }
  }
  END { exit(found_zero ? 0 : 1) }
' concrete.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Proves both SPEC.loop-inv and SPEC.incr-list.  The entry claim depends on
# loop-inv, so the required target run intentionally does not filter claims.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  | tee full-proof.out

if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY \
    > vacuity.out 2>&1
then
  echo "ERROR: false-postcondition probe unexpectedly proved" >&2
  exit 1
else
  vacuity_status=$?
  printf '%s\n' "$vacuity_status" > vacuity.exit
  rg -q 'WarnStuckClaimState' vacuity.out
fi

if kprove spec-body-mutant.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTANT \
    > body-mutant.out 2>&1
then
  echo "ERROR: changed-body probe unexpectedly proved" >&2
  exit 1
else
  body_mutant_status=$?
  printf '%s\n' "$body_mutant_status" > body-mutant.exit
  rg -q 'WarnStuckClaimState' body-mutant.out
fi

python3 differential.py | tee differential.out
