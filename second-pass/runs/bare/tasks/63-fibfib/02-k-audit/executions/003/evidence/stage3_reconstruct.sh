#!/usr/bin/env bash
set -u

candidate_src=/tmp/audit-work/63-fibfib/candidate-src
evidence=/audit-output/evidence
overall=0
cd "$candidate_src" || exit 125

printf '%s\n' \
  'COMMAND: kompile --backend llvm semantic.k --main-module FIBFIB --syntax-module FIBFIB-SYNTAX --output-definition concrete-kompiled'
kompile --backend llvm semantic.k \
  --main-module FIBFIB \
  --syntax-module FIBFIB-SYNTAX \
  --output-definition concrete-kompiled \
  >"$evidence/stage3_concrete_build.log" 2>&1
concrete_build_status=$?
printf 'EXIT: %s\n' "$concrete_build_status"
sed -n '1,240p' "$evidence/stage3_concrete_build.log"
if (( concrete_build_status != 0 )); then overall=1; fi

if (( concrete_build_status == 0 )); then
  printf '%s\n' \
    'COMMAND: python3 /audit-output/evidence/semantics_concrete_compare.py'
  python3 "$evidence/semantics_concrete_compare.py" \
    >"$evidence/stage3_concrete_execution.log" 2>&1
  concrete_execution_status=$?
  printf 'EXIT: %s\n' "$concrete_execution_status"
  sed -n '1,320p' "$evidence/stage3_concrete_execution.log"
  if (( concrete_execution_status != 0 )); then overall=1; fi
fi

printf '%s\n' \
  'COMMAND: kompile --backend haskell semantic.k --main-module FIBFIB --syntax-module FIBFIB-SYNTAX --output-definition proof-kompiled'
kompile --backend haskell semantic.k \
  --main-module FIBFIB \
  --syntax-module FIBFIB-SYNTAX \
  --output-definition proof-kompiled \
  >"$evidence/stage3_proof_build.log" 2>&1
proof_build_status=$?
printf 'EXIT: %s\n' "$proof_build_status"
sed -n '1,260p' "$evidence/stage3_proof_build.log"
if (( proof_build_status != 0 )); then overall=1; fi

if (( proof_build_status == 0 )); then
  for claim in FIBFIB-SPEC.program-correct FIBFIB-SPEC.loop-invariant; do
    safe_claim=${claim#FIBFIB-SPEC.}
    claim_log="$evidence/stage3_kprove_${safe_claim}.log"
    printf '%s\n' \
      "COMMAND: kprove spec.k --definition proof-kompiled --spec-module FIBFIB-SPEC --claims $claim -w none"
    kprove spec.k \
      --definition proof-kompiled \
      --spec-module FIBFIB-SPEC \
      --claims "$claim" \
      -w none >"$claim_log" 2>&1
    claim_status=$?
    printf 'EXIT: %s\n' "$claim_status"
    sed -n '1,320p' "$claim_log"
    if (( claim_status != 0 )) || ! grep -qx '#Top' "$claim_log"; then
      overall=1
    fi
  done

  printf '%s\n' \
    'COMMAND: kprove spec.k --definition proof-kompiled --spec-module FIBFIB-SPEC -w none'
  all_claims_log="$evidence/stage3_kprove_all.log"
  kprove spec.k \
    --definition proof-kompiled \
    --spec-module FIBFIB-SPEC \
    -w none >"$all_claims_log" 2>&1
  all_claims_status=$?
  printf 'EXIT: %s\n' "$all_claims_status"
  sed -n '1,320p' "$all_claims_log"
  if (( all_claims_status != 0 )) || ! grep -qx '#Top' "$all_claims_log"; then
    overall=1
  fi
fi

printf 'STAGE3_EXIT: %s\n' "$overall"
exit "$overall"
