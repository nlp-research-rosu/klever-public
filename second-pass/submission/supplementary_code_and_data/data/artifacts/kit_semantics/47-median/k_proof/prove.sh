#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate every generated source/proof artifact from the checked-in inputs.
python3 py2mpy.py solution.py > solution.mpy
python3 generate_program_k.py solution.py > program.k
python3 domain_checks.py | tee domain-checks.log
python3 py2mpy.py smoke.py > smoke.mpy
python3 generate_differential.py \
  > differential-smoke.py \
  2> differential-generation.log
python3 py2mpy.py differential-smoke.py > differential-smoke.mpy

# Concrete execution uses the required LLVM entry modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled | tee smoke-krun.log
krun differential-smoke.mpy \
  --definition runtime-kompiled \
  --output none
printf 'differential_krun_exit=0\n'

# Required positive symbolic target proof: all ten unbounded claims.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  | tee target-proof.log

# Gate A5: a false result for a realizable odd-list input must be rejected.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.log 2>&1
vacuity_status=$?
set -e
printf 'vacuity_exit=%s (expected nonzero)\n' "$vacuity_status"
if [[ "$vacuity_status" -eq 0 ]]; then
  echo "false-postcondition mutation unexpectedly proved" >&2
  exit 1
fi

# Gate A1: regenerate the proof binding from a body with a wrong odd return.
python3 py2mpy.py solution-mutant.py > solution-mutant.mpy
python3 generate_program_k.py \
  solution-mutant.py \
  MEDIAN-PROGRAM-MUTANT \
  solutionMedianClosureMutant \
  > program-mutant.k
kompile --backend haskell verification-mutant.k \
  --main-module VERIFICATION-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-mutant-kompiled
set +e
kprove spec-body-mutation.k \
  --definition verification-mutant-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation.log 2>&1
body_status=$?
set -e
printf 'body_mutation_exit=%s (expected nonzero)\n' "$body_status"
if [[ "$body_status" -eq 0 ]]; then
  echo "mutated implementation unexpectedly proved" >&2
  exit 1
fi
