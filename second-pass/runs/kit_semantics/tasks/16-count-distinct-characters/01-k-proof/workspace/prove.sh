#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 test_solution.py

rm -rf runtime-kompiled verification-kompiled

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled | tee concrete.out
grep -Fq '"empty_result" |-> 0' concrete.out
grep -Fq '"example_one_result" |-> 3' concrete.out
grep -Fq '"example_two_result" |-> 4' concrete.out

kast model-boundary.mpy \
  --definition runtime-kompiled \
  --module MPY-KRUN \
  --sort Module \
  --output kore > model-boundary.kore
krun model-boundary.kore \
  --parser cat \
  --definition runtime-kompiled | tee model-boundary.out
grep -Fq '"model_boundary_result" |-> 1' model-boundary.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee positive-proof.out
grep -Fxq '#Top' positive-proof.out

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > vacuity.out 2>&1
vacuity_status=$?
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1
body_mutation_status=$?
set -e

cat vacuity.out
printf 'VACUITY_EXIT=%s\n' "$vacuity_status"
cat body-mutation.out
printf 'BODY_MUTATION_EXIT=%s\n' "$body_mutation_status"

if [[ "$vacuity_status" -eq 0 ]]; then
  echo "The false postcondition unexpectedly proved." >&2
  exit 1
fi

if [[ "$body_mutation_status" -eq 0 ]]; then
  echo "The mutated function body unexpectedly proved." >&2
  exit 1
fi
