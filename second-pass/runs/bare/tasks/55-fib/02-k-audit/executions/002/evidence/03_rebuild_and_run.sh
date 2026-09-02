#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/55-fib-independent-audit
evidence=/audit-output/evidence
cd "$scratch"

test ! -e semantic-concrete-kompiled
test ! -e verification-proof-kompiled

printf '%s\n' 'COMMAND: kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition semantic-concrete-kompiled'
kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-concrete-kompiled \
  2>&1 | tee "$evidence/03_kompile_concrete.log"
printf 'EXIT_STATUS concrete_kompile=0\n'

printf '%s\n' 'COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-proof-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-proof-kompiled \
  2>&1 | tee "$evidence/03_kompile_proof.log"
printf 'EXIT_STATUS proof_kompile=0\n'

run_case() {
  local n="$1"
  local expected="$2"
  local output_file="$evidence/03_krun_n${n}.log"
  printf 'COMMAND: krun regenerated-solution.mpy --definition semantic-concrete-kompiled -cARG=%s --output pretty\n' "$n"
  krun regenerated-solution.mpy \
    --definition semantic-concrete-kompiled \
    -cARG="$n" \
    --output pretty \
    2>&1 | tee "$output_file"
  grep -Fq "    $expected ~> .K" "$output_file"
  printf 'CHECK K fib(%s)=%s EXIT_STATUS=0\n' "$n" "$expected"
}

run_case 0 0
run_case 1 1
run_case 2 1
run_case 8 21
run_case 10 55
run_case 12 144

printf '%s\n' 'COMMAND: kprove spec.k --definition verification-proof-kompiled --spec-module SPEC --claims SPEC.fib-invoke --output pretty'
kprove spec.k \
  --definition verification-proof-kompiled \
  --spec-module SPEC \
  --claims SPEC.fib-invoke \
  --output pretty \
  2>&1 | tee "$evidence/03_kprove_fib_invoke.log"
grep -qx '#Top' "$evidence/03_kprove_fib_invoke.log"
printf 'EXIT_STATUS fib-invoke=0 SIGNAL=#Top\n'

printf '%s\n' 'COMMAND: kprove spec.k --definition verification-proof-kompiled --spec-module SPEC --output pretty'
kprove spec.k \
  --definition verification-proof-kompiled \
  --spec-module SPEC \
  --output pretty \
  2>&1 | tee "$evidence/03_kprove_all_claims.log"
grep -qx '#Top' "$evidence/03_kprove_all_claims.log"
printf 'EXIT_STATUS all-positive-claims=0 SIGNAL=#Top\n'
