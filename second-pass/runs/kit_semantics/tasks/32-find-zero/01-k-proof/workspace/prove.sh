#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py solution-body-mutation.py > solution-body-mutation.mpy
python3 py2mpy.py solution.py | cmp - solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled
python3 validate.py

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-base-kompiled

diff -q \
  <(krun solution.mpy --definition verification-base-kompiled) \
  <(krun verification-program.mpy --definition verification-base-kompiled)

set +e
diff -q \
  <(krun solution-body-mutation.mpy --definition verification-base-kompiled) \
  <(krun verification-program.mpy --definition verification-base-kompiled)
body_mutation_status=$?
set -e

if [[ $body_mutation_status -eq 0 ]]; then
  echo "ERROR: material source-body mutation escaped the identity check" >&2
  exit 1
fi

echo "Expected source-body identity rejection observed (exit $body_mutation_status)."

kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module SPEC \
  --claims SPEC.find-load,SPEC.find-init

kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module SPEC-CONNECTION \
  --claims SPEC-CONNECTION.poly-loop-empty,SPEC-CONNECTION.poly-loop-int,SPEC-CONNECTION.poly-loop-float

kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module SPEC-CONNECTION \
  --claims SPEC-CONNECTION.poly-loop-empty,SPEC-CONNECTION.poly-loop-int,SPEC-CONNECTION.poly-loop-float,SPEC-CONNECTION.expand-loop

kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module SPEC-CONNECTION \
  --claims SPEC-CONNECTION.bisect-head

kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module SPEC-CONNECTION \
  --claims SPEC-CONNECTION.poly-loop-empty,SPEC-CONNECTION.poly-loop-int,SPEC-CONNECTION.poly-loop-float,SPEC-CONNECTION.bisect-loop

set +e
mutation_output="$(
  kprove spec-mutation.k \
    --definition verification-base-kompiled \
    --spec-module SPEC-MUTATION \
    --claims SPEC-MUTATION.wrong-poly-result 2>&1
)"
mutation_status=$?
set -e
printf '%s\n' "$mutation_output"

if [[ $mutation_status -eq 0 ]]; then
  echo "ERROR: deliberately false mutation unexpectedly proved" >&2
  exit 1
fi

if [[ $mutation_output != *"WarnStuckClaimState"* ]]; then
  echo "ERROR: mutation failed for an unexpected reason" >&2
  exit 1
fi

echo "Expected mutation rejection observed (exit $mutation_status)."
