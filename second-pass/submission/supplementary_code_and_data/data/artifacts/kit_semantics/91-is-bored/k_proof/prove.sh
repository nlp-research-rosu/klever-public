#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py model-boundary.py > model-boundary.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled > krun-smoke.out
python3 differential.py

python3 -c 'from solution import is_bored; value = is_bored("I\vwork"); assert value == 1; print(f"cpython vertical-tab result={value}")'
krun model-boundary.mpy --definition runtime-kompiled \
  > krun-model-boundary.out

kompile --backend haskell connection.k \
  --main-module CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC \
  | tee connection-proof.out

kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove loop-spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  | tee loop-proof.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore \
  > solution.kore
kast proof-program.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore \
  > proof-program.kore
cmp solution.kore proof-program.kore

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  | tee target-proof.out

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     > vacuity-mutation.out 2>&1; then
  echo "ERROR: off-by-one mutation unexpectedly proved" >&2
  exit 1
else
  rg -q 'WarnStuckClaimState' vacuity-mutation.out
  echo "EXPECTED FAILURE: off-by-one result mutation"
fi

kompile --backend haskell mutation.k \
  --main-module MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled
if kprove mutation-spec.k \
     --definition mutation-kompiled \
     --spec-module MUTATION-SPEC \
     > body-mutation.out 2>&1; then
  echo "ERROR: empty-loop-body mutation unexpectedly proved" >&2
  exit 1
else
  rg -q 'WarnStuckClaimState' body-mutation.out
  echo "EXPECTED FAILURE: material loop-body mutation"
fi

if kprove connection-mutation-spec.k \
     --definition connection-kompiled \
     --spec-module CONNECTION-MUTATION-SPEC \
     > connection-mutation.out 2>&1; then
  echo "ERROR: strip-to-upper mutation unexpectedly proved" >&2
  exit 1
else
  rg -q 'WarnStuckClaimState' connection-mutation.out
  echo "EXPECTED FAILURE: strip-to-upper connection mutation"
fi
