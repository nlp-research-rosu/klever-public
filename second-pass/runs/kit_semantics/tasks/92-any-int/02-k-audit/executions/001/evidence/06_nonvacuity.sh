#!/usr/bin/env bash
set +e
scratch=/tmp/audit-work/92-any-int-audit
evidence=/audit-output/evidence

printf '$ python3 /audit-output/evidence/06_false_witness.py\n'
python3 "$evidence/06_false_witness.py"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf '$ cp /audit-output/evidence/06_false_result_spec.k /tmp/audit-work/92-any-int-audit/\n'
cp "$evidence/06_false_result_spec.k" "$scratch/"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ kprove 06_false_result_spec.k --definition audit-verification-kompiled --spec-module AUDIT-FALSE-RESULT-SPEC --dry-run\n'
(
  cd "$scratch" || exit 125
  kprove 06_false_result_spec.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-FALSE-RESULT-SPEC \
    --dry-run
) > "$evidence/06_false_result_dry_run.log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
tail -n 120 "$evidence/06_false_result_dry_run.log"
if [ "$status" -ne 0 ]; then
  printf 'NONVACUITY_RESULT: MUTATION_DID_NOT_BUILD\n'
  exit 1
fi

printf '$ kprove 06_false_result_spec.k --definition audit-verification-kompiled --spec-module AUDIT-FALSE-RESULT-SPEC\n'
(
  cd "$scratch" || exit 125
  kprove 06_false_result_spec.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-FALSE-RESULT-SPEC
) > "$evidence/06_false_result_kprove.log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
tail -n 180 "$evidence/06_false_result_kprove.log"
if [ "$status" -eq 0 ]; then
  printf 'NONVACUITY_RESULT: UNEXPECTED_FALSE_PROOF_SUCCESS\n'
  exit 1
fi
if grep -q 'WarnStuckClaimState' "$evidence/06_false_result_kprove.log" &&
   grep -q '<k>' "$evidence/06_false_result_kprove.log" &&
   grep -q 'true' "$evidence/06_false_result_kprove.log"; then
  printf 'NONVACUITY_RESULT: EXPECTED_STUCK_TRUE_VS_FALSE\n'
  exit 0
fi
printf 'NONVACUITY_RESULT: WRONG_FAILURE_MODE\n'
exit 1
