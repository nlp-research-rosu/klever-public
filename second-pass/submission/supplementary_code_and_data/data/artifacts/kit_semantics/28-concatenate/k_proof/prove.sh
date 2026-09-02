#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

concatenate_krun_output="$(krun concrete_tests.mpy --definition runtime-kompiled)"
printf '%s\n' "$concatenate_krun_output"
printf '%s\n' "$concatenate_krun_output" | grep -F '"empty" |-> str ( .IntSeq )'
printf '%s\n' "$concatenate_krun_output" | grep -F '"example" |-> str ( iCons ( 97 , iCons ( 98 , iCons ( 99 , .IntSeq ) ) ) )'
printf '%s\n' "$concatenate_krun_output" | grep -F '"mixed" |-> str ( iCons ( 120 , iCons ( 121 , iCons ( 122 , .IntSeq ) ) ) )'

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

python3 differential_tests.py

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
concatenate_vacuity_status=$?
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
concatenate_body_status=$?
set -e

printf 'VACUITY_EXIT=%s\n' "$concatenate_vacuity_status"
printf 'BODY_MUTATION_EXIT=%s\n' "$concatenate_body_status"

if [ "$concatenate_vacuity_status" -eq 0 ]; then
  printf '%s\n' 'error: false-result mutation unexpectedly proved' >&2
  exit 1
fi
if [ "$concatenate_body_status" -eq 0 ]; then
  printf '%s\n' 'error: changed-body mutation unexpectedly proved' >&2
  exit 1
fi
