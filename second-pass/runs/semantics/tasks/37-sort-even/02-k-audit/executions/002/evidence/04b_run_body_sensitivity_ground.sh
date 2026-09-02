#!/usr/bin/env bash
set -u

scratch="/tmp/audit-work/37-sort-even"
evidence="/audit-output/evidence"
summary="$evidence/04b-body-sensitivity-ground-summary.log"
spec="$scratch/spec-step3-ground.k"
definition="$scratch/verification-step3-kompiled"

printf '%s\n' \
  'COMMAND: cp -a /audit-output/evidence/04-spec-step3-ground.k /tmp/audit-work/37-sort-even/spec-step3-ground.k' \
  > "$summary"
cp -a "$evidence/04-spec-step3-ground.k" "$spec" >> "$summary" 2>&1
copy_status=$?
printf 'COPY_EXIT_STATUS: %s\n' "$copy_status" >> "$summary"

correct_log="$evidence/04b-body-sensitivity-ground-correct.log"
printf '%s\n' \
  'COMMAND: timeout 180 kprove spec-step3-ground.k --definition verification-step3-kompiled --spec-module SPEC-STEP3-GROUND --claims SPEC-STEP3-GROUND.mutated-result --output pretty' \
  > "$correct_log"
if [ "$copy_status" -eq 0 ]; then
  (
    cd "$scratch" &&
    timeout 180 kprove spec-step3-ground.k \
      --definition "$definition" \
      --spec-module SPEC-STEP3-GROUND \
      --claims SPEC-STEP3-GROUND.mutated-result \
      --output pretty
  ) >> "$correct_log" 2>&1
  correct_status=$?
else
  correct_status=1
fi
printf 'EXIT_STATUS: %s\n' "$correct_status" >> "$correct_log"
printf 'MUTATED_CORRECT_RESULT_EXIT_STATUS: %s\n' "$correct_status" >> "$summary"

wrong_log="$evidence/04b-body-sensitivity-ground-wrong.log"
printf '%s\n' \
  'COMMAND: timeout 180 kprove spec-step3-ground.k --definition verification-step3-kompiled --spec-module SPEC-STEP3-GROUND --claims SPEC-STEP3-GROUND.original-result --output pretty' \
  > "$wrong_log"
if [ "$copy_status" -eq 0 ]; then
  (
    cd "$scratch" &&
    timeout 180 kprove spec-step3-ground.k \
      --definition "$definition" \
      --spec-module SPEC-STEP3-GROUND \
      --claims SPEC-STEP3-GROUND.original-result \
      --output pretty
  ) >> "$wrong_log" 2>&1
  wrong_status=$?
else
  wrong_status=0
fi
printf 'EXIT_STATUS: %s\n' "$wrong_status" >> "$wrong_log"
printf 'EXPECTED_NONZERO_ORIGINAL_RESULT_EXIT_STATUS: %s\n' "$wrong_status" >> "$summary"

wrong_stuck=1
if rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check.*failed' "$wrong_log"; then
  wrong_stuck=0
fi
printf 'EXPECTED_STUCK_RESIDUAL_CHECK_EXIT_STATUS: %s\n' "$wrong_stuck" >> "$summary"

if [ "$copy_status" -ne 0 ] || [ "$correct_status" -ne 0 ] || \
   [ "$wrong_status" -eq 0 ] || [ "$wrong_status" -eq 124 ] || \
   [ "$wrong_stuck" -ne 0 ]; then
  printf '%s\n' 'OVERALL_EXIT_STATUS: 1' >> "$summary"
  exit 1
fi
printf '%s\n' 'OVERALL_EXIT_STATUS: 0' >> "$summary"
exit 0
