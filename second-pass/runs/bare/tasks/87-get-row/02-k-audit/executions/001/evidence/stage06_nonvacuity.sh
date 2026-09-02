#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/87-get-row
spec="$scratch/source/spec-vacuity-audit.k"
definition="$scratch/verification-audit-kompiled"
status=0

printf '%s\n' '$ kprove false mutation with --dry-run (parse/build only)'
dry_output="$(
  kprove "$spec" \
    --definition "$definition" \
    --spec-module SPEC-VACUITY-AUDIT \
    --dry-run 2>&1
)"
dry_rc=$?
printf '%s\n' "$dry_output"
printf 'mutation_dry_run_exit=%d\n' "$dry_rc"
if (( dry_rc != 0 )); then
  status=1
fi

printf '%s\n' '$ kprove meaningful false empty-input result mutation'
proof_output="$(
  kprove "$spec" \
    --definition "$definition" \
    --spec-module SPEC-VACUITY-AUDIT 2>&1
)"
proof_rc=$?
printf '%s\n' "$proof_output"
printf 'mutation_proof_exit=%d\n' "$proof_rc"
stuck_count="$(printf '%s\n' "$proof_output" | grep -c 'WarnStuckClaimState')"
printf 'warn_stuck_count=%s\n' "$stuck_count"

if (( proof_rc == 0 )) || (( stuck_count < 1 )); then
  status=1
fi

printf 'overall_exit=%d\n' "$status"
exit "$status"
