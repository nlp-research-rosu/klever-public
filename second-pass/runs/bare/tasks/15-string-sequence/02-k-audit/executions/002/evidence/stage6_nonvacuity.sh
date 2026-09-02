#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
definition="$scratch/verification-haskell-kompiled"
export PATH="/home/agent/.nix-profile/bin:$PATH"
cp /audit-output/evidence/spec-vacuity-audit.k \
  "$scratch/spec-vacuity-audit.k"

printf 'COMMAND: bash /audit-output/evidence/stage6_nonvacuity.sh\n'
printf 'MUTATION: at satisfying input n=0, change the required return from SVal("0") to SVal("1").\n'
printf 'WITNESS: canonical(0) = candidate(0) = "0" (stage2-fidelity.log).\n'

printf 'COMMAND: cd %s && kprove spec-vacuity-audit.k --definition %s --spec-module SPEC-VACUITY-AUDIT --dry-run\n' \
  "$scratch" "$definition"
dry_output="$(
  cd "$scratch" &&
  kprove spec-vacuity-audit.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY-AUDIT \
    --dry-run \
    2>&1
)"
dry_status=$?
printf '%s\n' "$dry_output"
printf 'dry_run_exit=%s\n' "$dry_status"

printf 'COMMAND: cd %s && kprove spec-vacuity-audit.k --definition %s --spec-module SPEC-VACUITY-AUDIT\n' \
  "$scratch" "$definition"
proof_output="$(
  cd "$scratch" &&
  kprove spec-vacuity-audit.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY-AUDIT \
    2>&1
)"
proof_status=$?
printf '%s\n' "$proof_output"
printf 'mutated_kprove_exit=%s\n' "$proof_status"
residual_status=1
if printf '%s\n' "$proof_output" | rg \
  'WarnStuckClaimState|doesn.t unify with the destination|implication check' \
  >/dev/null
then
  residual_status=0
fi
printf 'expected_unmet_result_residual=%s\n' "$((1 - residual_status))"

final_status=0
if [[
  "$dry_status" != 0 ||
  "$proof_status" == 0 ||
  "$residual_status" != 0
]]; then
  final_status=1
fi
printf 'SCRIPT_EXIT=%s\n' "$final_status"
exit "$final_status"
