#!/usr/bin/env bash
set -u
set -o pipefail
set -x

PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence
overall=0

cp "$work/verification.k" "$work/verification-body-mutant.k"
patch --forward "$work/verification-body-mutant.k" \
  < "$evidence/body-mutation.patch"
patch_status=$?
printf 'BODY_PATCH_EXIT=%s\n' "$patch_status"
(( patch_status == 0 )) || overall=1
cp "$evidence/body-mutant-spec.k" "$work/body-mutant-spec.k"

kompile "$work/verification-body-mutant.k" \
  --backend haskell \
  --main-module SPECIALFILTER-VERIFICATION-LOOP \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/body-mutant-kompiled" \
  2>&1 | tee "$evidence/stage5_body_mutant_build.log"
status=${PIPESTATUS[0]}
printf 'BODY_MUTANT_BUILD_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

if (( status == 0 )); then
  kprove "$work/body-mutant-spec.k" \
    --definition "$work/body-mutant-kompiled" \
    --spec-module SPECIALFILTER-BODY-MUTANT-SPEC \
    2>&1 | tee "$evidence/stage5_body_mutant_proof.log"
  proof_status=${PIPESTATUS[0]}
  printf 'BODY_MUTANT_PROOF_EXIT=%s\n' "$proof_status"
  if (( proof_status == 0 )); then
    printf 'UNEXPECTED_BODY_MUTANT_PROOF_SUCCESS\n'
    overall=1
  fi
  grep -q 'WarnStuckClaimState' "$evidence/stage5_body_mutant_proof.log"
  stuck_status=$?
  printf 'BODY_MUTANT_STUCK_CHECK_EXIT=%s\n' "$stuck_status"
  (( stuck_status == 0 )) || overall=1
fi

printf 'EXPECTED_BODY_MUTANT_PROOF_NONZERO=%s\n' "${proof_status:-not-run}"
printf 'BODY_SENSITIVITY_OVERALL_EXIT=%s\n' "$overall"
exit "$overall"
