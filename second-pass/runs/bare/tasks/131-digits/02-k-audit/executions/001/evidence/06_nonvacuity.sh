#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/131-digits
proofdef="$scratch/verification-fresh-kompiled"
failures=0

printf 'AUDIT STAGE 6: FRESH NON-VACUITY MUTATION\n'

printf '\n$ cp %q %q\n' \
  /audit-output/evidence/06_false_result_mutation.k \
  "$scratch/06_false_result_mutation.k"
cp /audit-output/evidence/06_false_result_mutation.k \
  "$scratch/06_false_result_mutation.k"
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then failures=1; fi

printf '\nSatisfying concrete witness and false expected value:\n'
printf '$ python3 /audit-output/evidence/03_python_case.py 235\n'
python3 /audit-output/evidence/03_python_case.py 235
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then failures=1; fi
printf 'mutated_required_answer=16\n'

printf '\n$ timeout 300s kprove %q --definition %q --spec-module SPEC-VACUITY-AUDIT --dry-run\n' \
  "$scratch/06_false_result_mutation.k" "$proofdef"
dry_output=$(timeout 300s kprove "$scratch/06_false_result_mutation.k" \
  --definition "$proofdef" --spec-module SPEC-VACUITY-AUDIT --dry-run 2>&1)
dry_status=$?
printf '%s\n[exit %d]\n' "$dry_output" "$dry_status"
if (( dry_status != 0 )); then
  printf 'mutation_build=FAIL\n'
  failures=1
else
  printf 'mutation_build=PASS\n'
fi

printf '\n$ timeout 300s kprove %q --definition %q --spec-module SPEC-VACUITY-AUDIT\n' \
  "$scratch/06_false_result_mutation.k" "$proofdef"
proof_output=$(timeout 300s kprove "$scratch/06_false_result_mutation.k" \
  --definition "$proofdef" --spec-module SPEC-VACUITY-AUDIT 2>&1)
proof_status=$?
printf '%s\n[exit %d]\n' "$proof_output" "$proof_status"

if (( proof_status == 0 )); then
  printf 'nonvacuity=FAIL (false mutation proved)\n'
  failures=1
elif (( proof_status == 124 )); then
  printf 'nonvacuity=FAIL (timeout is not proof rejection)\n'
  failures=1
elif ! printf '%s\n' "$proof_output" | grep -q 'WarnStuckClaimState'; then
  printf 'nonvacuity=FAIL (no stuck-claim residual)\n'
  failures=1
elif ! printf '%s\n' "$proof_output" | grep -Eq \
  'oddProduct|LbloddProduct|\\+Int|plusInt|Plus.*Int|#Equals'; then
  printf 'nonvacuity=FAIL (residual does not expose result obligation)\n'
  failures=1
else
  printf 'nonvacuity=PASS (built, reached, and rejected false result obligation)\n'
fi

printf '\nstage6_failures=%d\n' "$failures"
exit "$failures"
