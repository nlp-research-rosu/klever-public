#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/71-triangle-area
proof="$scratch/build/proof-kompiled"
probe_output="$scratch/non-vacuity-proof-output.log"
overall=0

printf 'Audit stage 6: fresh non-vacuity mutation\n'
printf 'Satisfying witness: Args(VInt(3),VInt(4),VInt(5)); actual result 600 hundredths.\n'
printf 'Mutation: result obligation changed from VRounded(600) to VRounded(601).\n'

printf '\n$ kprove %s/spec-vacuity.k --definition %s --spec-module SPEC-VACUITY --claims SPEC-VACUITY.false-result-3-4-5 --dry-run\n' \
  "$scratch" "$proof"
kprove "$scratch/spec-vacuity.k" \
  --definition "$proof" \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-result-3-4-5 \
  --dry-run
dry_status=$?
printf '[exit_status] %d\n' "$dry_status"
(( dry_status == 0 )) || overall=1

printf '\n$ kprove %s/spec-vacuity.k --definition %s --spec-module SPEC-VACUITY --claims SPEC-VACUITY.false-result-3-4-5 --smt-timeout 10000\n' \
  "$scratch" "$proof"
kprove "$scratch/spec-vacuity.k" \
  --definition "$proof" \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-result-3-4-5 \
  --smt-timeout 10000 > "$probe_output" 2>&1
proof_status=$?
sed -n '1,240p' "$probe_output"
printf '[exit_status] %d\n' "$proof_status"

if (( proof_status == 0 )); then
  printf 'ERROR: false mutation unexpectedly closed.\n'
  overall=1
fi

if rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check.*failed' \
  "$probe_output"; then
  printf 'expected_unmet_obligation_residual=yes\n'
else
  printf 'expected_unmet_obligation_residual=no\n'
  overall=1
fi

printf '\n[script_exit_status] %d\n' "$overall"
exit "$overall"
