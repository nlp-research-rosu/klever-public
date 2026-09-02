#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/64-vowels-count

kast solution.mpy \
  --definition audit-verification-kompiled \
  --module SOLUTION \
  --sort Program \
  --expand-macros \
  --output kore \
  --output-file solution-expanded.kore
solution_kast_status=$?
printf 'SOLUTION_KAST_EXIT_STATUS=%d\n' "$solution_kast_status"

kast \
  --expression solutionProgram \
  --definition audit-verification-kompiled \
  --module SOLUTION \
  --sort Program \
  --expand-macros \
  --output kore \
  --output-file macro-expanded.kore
macro_kast_status=$?
printf 'MACRO_KAST_EXIT_STATUS=%d\n' "$macro_kast_status"

cmp -s solution-expanded.kore macro-expanded.kore
constructor_compare_status=$?
printf 'CONSTRUCTOR_COMPARE_EXIT_STATUS=%d\n' "$constructor_compare_status"
sha256sum solution-expanded.kore macro-expanded.kore
cp solution-expanded.kore /audit-output/evidence/solution-expanded.kore
cp macro-expanded.kore /audit-output/evidence/macro-expanded.kore

cp /audit-output/evidence/spec-concrete-witness.k audit-spec-concrete-witness.k
kprove audit-spec-concrete-witness.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-CONCRETE-WITNESS \
  --output pretty
concrete_claims_status=$?
printf 'CONCRETE_CLAIMS_EXIT_STATUS=%d\n' "$concrete_claims_status"

python3 /audit-output/evidence/pinning_python_witness.py
python_witness_status=$?
printf 'PYTHON_WITNESS_EXIT_STATUS=%d\n' "$python_witness_status"

cd /tmp/audit-work/64-vowels-count/body-mutant
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition body-mutant-kompiled
body_mutant_build_status=$?
printf 'BODY_MUTANT_BUILD_EXIT_STATUS=%d\n' "$body_mutant_build_status"

timeout 60 kprove spec.k \
  --definition body-mutant-kompiled \
  --spec-module SPEC \
  --claims SPEC.vowels-count-correct \
  --output pretty \
  > body-mutant-kprove.raw.log 2>&1
body_mutant_proof_status=$?
printf 'BODY_MUTANT_PROOF_EXIT_STATUS=%d\n' "$body_mutant_proof_status"
sed -n '1,260p' body-mutant-kprove.raw.log
cp body-mutant-kprove.raw.log /audit-output/evidence/body-mutant-kprove.raw.log
rg -q 'WarnStuckClaimState' body-mutant-kprove.raw.log
body_mutant_stuck_residual_status=$?
printf 'BODY_MUTANT_STUCK_RESIDUAL_PRESENT=%d\n' "$body_mutant_stuck_residual_status"

if (( solution_kast_status != 0 )); then exit "$solution_kast_status"; fi
if (( macro_kast_status != 0 )); then exit "$macro_kast_status"; fi
if (( constructor_compare_status != 0 )); then exit "$constructor_compare_status"; fi
if (( concrete_claims_status != 0 )); then exit "$concrete_claims_status"; fi
if (( python_witness_status != 0 )); then exit "$python_witness_status"; fi
if (( body_mutant_build_status != 0 )); then exit "$body_mutant_build_status"; fi
if (( body_mutant_proof_status == 0 )); then exit 91; fi
if (( body_mutant_proof_status == 124 )); then exit 92; fi
if (( body_mutant_stuck_residual_status != 0 )); then exit 93; fi

