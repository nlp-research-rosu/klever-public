#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$work"

cp "$evidence/06_false_result_spec.k" "$work/06_false_result_spec.k"

dry_log="$evidence/06_false_result_dry_run.log"
{
  printf '$ kprove 06_false_result_spec.k --definition verification-audit-kompiled --spec-module AUDIT-FALSE-RESULT-SPEC --dry-run\n'
  kprove 06_false_result_spec.k \
    --definition verification-audit-kompiled \
    --spec-module AUDIT-FALSE-RESULT-SPEC \
    --dry-run
  status=$?
  printf '\n[exit %d]\n' "$status"
} > "$dry_log" 2>&1
dry_status=$status

proof_log="$evidence/06_false_result_proof.log"
{
  printf '$ kprove 06_false_result_spec.k --definition verification-audit-kompiled --spec-module AUDIT-FALSE-RESULT-SPEC\n'
  kprove 06_false_result_spec.k \
    --definition verification-audit-kompiled \
    --spec-module AUDIT-FALSE-RESULT-SPEC
  status=$?
  printf '\n[exit %d]\n' "$status"
} > "$proof_log" 2>&1
proof_status=$status

summary="$evidence/06_nonvacuity_summary.log"
{
  printf 'witness=[0,1,2,3]\n'
  printf 'witness_precondition=all elements are nonnegative Int; length=4\n'
  printf 'trusted_canonical='
  python3 -c 'import sys; sys.path.insert(0, "/reference"); from canonical import is_sorted; print(is_sorted([0,1,2,3]))'
  printf 'generated_solution='
  python3 -c 'import sys; sys.path.insert(0, "/tmp/audit-work/reconstruction"); from solution import is_sorted; print(is_sorted([0,1,2,3]))'
  printf 'mutated_required_result=false\n'
  printf 'dry_run_exit=%d\n' "$dry_status"
  printf 'proof_exit=%d\n' "$proof_status"
  printf 'warn_stuck_count=%s\n' "$(rg -c 'WarnStuckClaimState' "$proof_log" || true)"
  printf 'top_count=%s\n' "$(rg -c '^#Top$' "$proof_log" || true)"
  printf 'dry_log=%s\n' "$dry_log"
  printf 'proof_log=%s\n' "$proof_log"
} > "$summary"

cat "$summary"
test "$dry_status" -eq 0
test "$proof_status" -ne 0
rg -q 'WarnStuckClaimState' "$proof_log"
! rg -q '^#Top$' "$proof_log"
