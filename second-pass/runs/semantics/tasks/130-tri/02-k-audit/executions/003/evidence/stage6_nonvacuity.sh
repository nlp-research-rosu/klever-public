#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/130-tri-audit
evidence=/audit-output/evidence
spec="$evidence/spec_vacuity.k"
definition="$scratch/verification-audit-kompiled"
dry_log="$evidence/stage6_vacuity_dry_run.full.log"
proof_log="$evidence/stage6_vacuity_proof.full.log"
overall=0

printf 'MUTATION: entry postcondition prefixIndex(result) == N + 1\n'
printf 'SATISFYING_WITNESS: N=0; Python candidate and canonical both return value-equivalent [1], candidate prefixIndex base equation yields 0\n'

printf '\nCOMMAND: kprove %q --definition %q --spec-module TRI-VACUITY-SPEC --dry-run\n' \
  "$spec" "$definition"
kprove "$spec" \
  --definition "$definition" \
  --spec-module TRI-VACUITY-SPEC \
  --dry-run \
  --output pretty >"$dry_log" 2>&1
status=$?
printf 'EXIT_STATUS: %d EXPECTED: 0\n' "$status"
if [[ $(wc -l < "$dry_log") -le 160 ]]; then
  sed -n '1,160p' "$dry_log"
else
  sed -n '1,80p' "$dry_log"
  printf '%s\n' '... OUTPUT BOUNDED; FULL LOG PRESERVED ...'
  tail -n 80 "$dry_log"
fi
if [[ "$status" -ne 0 ]]; then overall=1; fi

printf '\nCOMMAND: kprove %q --definition %q --spec-module TRI-VACUITY-SPEC --output pretty\n' \
  "$spec" "$definition"
kprove "$spec" \
  --definition "$definition" \
  --spec-module TRI-VACUITY-SPEC \
  --output pretty >"$proof_log" 2>&1
status=$?
printf 'EXIT_STATUS: %d EXPECTED: nonzero\n' "$status"
if [[ $(wc -l < "$proof_log") -le 260 ]]; then
  sed -n '1,260p' "$proof_log"
else
  sed -n '1,130p' "$proof_log"
  printf '%s\n' '... OUTPUT BOUNDED; FULL LOG PRESERVED ...'
  tail -n 130 "$proof_log"
fi
if [[ "$status" -eq 0 ]]; then overall=1; fi
if ! grep -q 'WarnStuckClaimState' "$proof_log"; then
  printf 'EXPECTED_STUCK_RESIDUAL_MISSING\n'
  overall=1
fi
if grep -Eq 'Parse error|Could not find|FileNotFound|Critical:' "$proof_log"; then
  printf 'UNRELATED_FAILURE_DETECTED\n'
  overall=1
fi

printf '\nSTAGE6_NONVACUITY_EXIT_STATUS: %d\n' "$overall"
exit "$overall"
