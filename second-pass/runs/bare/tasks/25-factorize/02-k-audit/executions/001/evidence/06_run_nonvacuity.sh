#!/usr/bin/env bash
set -uo pipefail

source_dir=/tmp/audit-work/25-factorize-audit/source
spec_file="$source_dir/audit-false-spec.k"
preserved_spec=/audit-output/evidence/06_audit_false_spec.k
definition=/tmp/audit-work/25-factorize-audit/verification-fresh-kompiled
dry_log=/audit-output/evidence/06_false_mutation_dry_run.log
proof_log=/audit-output/evidence/06_false_mutation_proof.log

cd "$source_dir" || exit 1

echo "$ cmp $spec_file $preserved_spec"
cmp "$spec_file" "$preserved_spec"
status=$?
printf '[exit_status=%d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

{
  echo "$ kprove $spec_file --definition $definition --spec-module AUDIT-FALSE-SPEC --dry-run"
  kprove "$spec_file" \
    --definition "$definition" \
    --spec-module AUDIT-FALSE-SPEC \
    --dry-run
  dry_status=$?
  printf '[exit_status=%d]\n' "$dry_status"
} >"$dry_log" 2>&1
dry_status=$(sed -n 's/^\[exit_status=\([0-9][0-9]*\)\]$/\1/p' "$dry_log" | tail -1)
printf 'dry_run_exit_status=%s log=%s\n' "$dry_status" "$dry_log"
if [[ "$dry_status" != 0 ]]; then
  tail -60 "$dry_log"
  exit 1
fi

{
  echo "$ kprove $spec_file --definition $definition --spec-module AUDIT-FALSE-SPEC"
  kprove "$spec_file" \
    --definition "$definition" \
    --spec-module AUDIT-FALSE-SPEC
  proof_status=$?
  printf '[exit_status=%d]\n' "$proof_status"
} >"$proof_log" 2>&1
proof_status=$(sed -n 's/^\[exit_status=\([0-9][0-9]*\)\]$/\1/p' "$proof_log" | tail -1)

if rg -q 'WarnStuckClaimState' "$proof_log"; then
  stuck=yes
else
  stuck=no
fi
if rg -Fxq '#Top' "$proof_log"; then
  top=yes
else
  top=no
fi

printf 'proof_exit_status=%s stuck_warning=%s printed_exact_top=%s log=%s\n' \
  "$proof_status" "$stuck" "$top" "$proof_log"
tail -60 "$proof_log"

if [[ "$proof_status" == 0 || "$stuck" != yes || "$top" != no ]]; then
  exit 1
fi
