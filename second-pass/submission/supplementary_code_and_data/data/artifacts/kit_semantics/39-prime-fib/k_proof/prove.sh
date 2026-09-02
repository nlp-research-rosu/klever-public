#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 test_solution.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

# Prove the nested loop first.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop

# Prove the outer loop using the already-proved inner claim as a staged lemma.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop \
  --trusted SPEC.inner-loop

# Prove the entry claim using the two already-proved loop claims.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC.prime-fib \
  --trusted SPEC.inner-loop,SPEC.outer-loop

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC-VACUITY.false-result \
  --trusted SPEC.inner-loop,SPEC.outer-loop
then
  echo "ERROR: false-result mutation unexpectedly proved"
  exit 1
else
  mutation_status=$?
  echo "EXPECTED FAILURE: false-result mutation exited ${mutation_status}"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC-BODY-MUTATION.changed-initial-b \
  --trusted SPEC.inner-loop,SPEC.outer-loop
then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
else
  body_mutation_status=$?
  echo "EXPECTED FAILURE: body mutation exited ${body_mutation_status}"
fi
