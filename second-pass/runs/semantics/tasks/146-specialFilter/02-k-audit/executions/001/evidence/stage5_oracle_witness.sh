#!/usr/bin/env bash
set -u
set -o pipefail
set -x

PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence
overall=0

cp "$evidence/oracle-witness.k" "$work/oracle-witness.k"
cp "$evidence/oracle-witness-spec.k" "$work/oracle-witness-spec.k"

kompile "$work/oracle-witness.k" \
  --backend haskell \
  --main-module OPPOSITE-DECIMAL-INTERPRETATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/oracle-witness-symbolic-kompiled" \
  2>&1 | tee "$evidence/stage5_oracle_witness_symbolic_build.log"
status=${PIPESTATUS[0]}
printf 'ORACLE_WITNESS_BUILD_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

if (( status == 0 )); then
  kprove "$work/oracle-witness-spec.k" \
    --definition "$work/oracle-witness-symbolic-kompiled" \
    --spec-module OPPOSITE-DECIMAL-INTERPRETATION-SPEC \
    2>&1 | tee "$evidence/stage5_oracle_witness_symbolic_proof.log"
  status=${PIPESTATUS[0]}
  printf 'ORACLE_WITNESS_PROOF_EXIT=%s\n' "$status"
  (( status == 0 )) || overall=1
  if ! grep -qx '#Top' "$evidence/stage5_oracle_witness_symbolic_proof.log"; then
    printf 'ORACLE_WITNESS_EXACT_TOP_NOT_FOUND\n'
    overall=1
  fi
fi

printf 'ORACLE_WITNESS_OVERALL_EXIT=%s\n' "$overall"
exit "$overall"
