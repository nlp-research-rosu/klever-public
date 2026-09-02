#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/160-do-algebra
proof_log=/audit-output/evidence/06_false_mutation_kprove.log
cp /audit-output/evidence/06_false_mutation.k "$scratch/06_false_mutation.k"

command=(
  kprove "$scratch/06_false_mutation.k"
  --definition "$scratch/audit-verification-kompiled"
  --spec-module AUDIT-FALSE-MUTATION
)
printf 'COMMAND:'
printf ' %q' "${command[@]}"
printf '\n'
{
  printf 'COMMAND:'
  printf ' %q' "${command[@]}"
  printf '\n'
} > "$proof_log"
"${command[@]}" 2>&1 | tee -a "$proof_log"
proof_status=${PIPESTATUS[0]}
printf 'KPROVE_EXIT_STATUS=%d\n' "$proof_status" | tee -a "$proof_log"

if (( proof_status == 0 )); then
  echo "ERROR: false answer 8 unexpectedly proved"
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$proof_log"; then
  echo "ERROR: failure was not a stuck reachability obligation"
  exit 2
fi
if ! rg -q '"answer".*\\|-> 9' "$proof_log"; then
  echo "ERROR: residual did not expose the expected actual answer 9"
  exit 3
fi
echo "EXPECTED_FAILURE_CONFIRMED: reachable final answer is 9, not demanded 8"
exit 0
