#!/usr/bin/env bash
set -u
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

root=/tmp/audit-work/130-tri
definition="$root/build/verification-kompiled"
spec=/audit-output/evidence/spec-vacuity-audit.k
dry_run_output="$root/build/spec-vacuity-audit.kore"
proof_output="$root/build/spec-vacuity-audit.proof.log"

kprove "$spec" \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run > "$dry_run_output" 2>&1
dry_run_status=$?
printf 'mutation_dry_run_status=%s\n' "$dry_run_status"
wc -l -c "$dry_run_output"
sha256sum "$dry_run_output"

kprove "$spec" \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-VACUITY \
  > "$proof_output" 2>&1
proof_status=$?
printf 'mutation_proof_status=%s\n' "$proof_status"
wc -l -c "$proof_output"
sed -n '1,160p' "$proof_output"

grep -q 'WarnStuckClaimState' "$proof_output"
stuck_status=$?
grep -q 'triPrefix' "$proof_output"
result_obligation_status=$?
printf 'stuck_residual_present=%s result_obligation_present=%s\n' \
  "$stuck_status" "$result_obligation_status"

if (( dry_run_status == 0 \
      && proof_status != 0 \
      && stuck_status == 0 \
      && result_obligation_status == 0 )); then
  printf 'fresh_nonvacuity_pass=true witness_N=0 actual=[1] mutated=[1,3]\n'
  exit 0
fi

printf 'fresh_nonvacuity_pass=false\n'
exit 1
