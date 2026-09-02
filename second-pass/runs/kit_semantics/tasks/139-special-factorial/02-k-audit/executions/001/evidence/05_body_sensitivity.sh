#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction

printf '%s\n' 'COMMAND: kprove spec-body-mutation.k --definition audit-verification-kompiled --spec-module SPEC-BODY-MUTATION'
kprove spec-body-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
proof_status=$?
printf 'MUTATED_PROOF_EXIT: %s\n' "$proof_status"

# Re-run into a bounded reviewer log so the expected residual can be checked
# without trusting the candidate's saved output.
kprove spec-body-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION > /tmp/audit-work/reconstruction/audit-body-sensitivity.residual 2>&1
residual_status=$?
printf 'RESIDUAL_CAPTURE_EXIT: %s\n' "$residual_status"
rg -n 'WarnStuckClaimState|R \*Int \( F \*Int I \) \+Int 1|backend terminated' \
  /tmp/audit-work/reconstruction/audit-body-sensitivity.residual
match_status=$?
printf 'EXPECTED_RESIDUAL_MATCH_EXIT: %s\n' "$match_status"
sed -n '1,180p' /tmp/audit-work/reconstruction/audit-body-sensitivity.residual

if [ "$proof_status" -eq 0 ] || [ "$residual_status" -eq 0 ] || [ "$match_status" -ne 0 ]; then
  exit 1
fi
exit 0
